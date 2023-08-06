"""PyTestRunner class and related functions."""
from concurrent import futures
import logging
import os
import multiprocessing
import queue
import subprocess
from typing import Tuple, Dict, Callable, List, Union
import pprint

import eventlet  # type: ignore
import flask_socketio  # type: ignore

import pytest  # type: ignore
from _pytest import reports  # type: ignore

from pytest_web_ui import result_tree

LOGGER = logging.getLogger(__name__)
_DONE = 0xDEAD


class PyTestRunner:
    """Owns the test result tree and handles running tests and updating the results."""

    _ACTIVE_LOOP_SLEEP = 0.1  # seconds

    def __init__(
        self, directory: str, socketio: flask_socketio.SocketIO, use_docker: bool
    ):
        self._directory = directory
        self.result_tree, self._result_index = _init_result_tree(directory)
        self._socketio = socketio
        self._branch_schema = result_tree.BranchNodeSchema()
        self._leaf_schema = result_tree.LeafNodeSchema()
        self.environment = EnvironmentManager(directory, use_docker)

    def run_tests(self, nodeid: str):
        """
        Run the test or tests for a given PyTest node. Updates the results tree with
        test reports as they are available.
        """
        result_node = self._result_index[nodeid]
        result_node.status = result_tree.TestState.RUNNING
        self._send_update(result_node)
        self._socketio.start_background_task(self._run_test, nodeid)

    def _run_test(self, nodeid: str):
        result_queue: "multiprocessing.Queue[Union[reports.TestReport, int]]" = multiprocessing.Queue()
        proc = multiprocessing.context.SpawnContext.Process(
            target=_run_test,
            args=(nodeid, result_queue, self.result_tree.fspath, self._directory),
        )
        proc.start()

        while True:
            try:
                val = result_queue.get_nowait()
                if val == _DONE:
                    break
                self._add_test_report(val)
            except queue.Empty:
                eventlet.sleep(self._ACTIVE_LOOP_SLEEP)

        self._send_update(self._result_index[nodeid])

    def _add_test_report(self, report: reports.TestReport):
        """Add a test report into our result tree."""
        result_node = self._result_index[report.nodeid]
        assert isinstance(result_node, result_tree.LeafNode)
        result_node.report = report

    def _send_update(self, updated_node: result_tree.Node):
        if updated_node.nodeid == self.result_tree.nodeid:
            parents_slice = self._branch_schema.dump(updated_node)
        else:
            parents_slice, parent_node = result_tree.serialize_parents_slice(
                updated_node, self.result_tree
            )

            if isinstance(updated_node, result_tree.BranchNode):
                serialized_result = self._branch_schema.dump(updated_node)
                parent_node["child_branches"] = {
                    updated_node.short_id: serialized_result
                }
            elif isinstance(updated_node, result_tree.LeafNode):
                serialized_result = self._leaf_schema.dump(updated_node)
                parent_node["child_leaves"] = {updated_node.short_id: serialized_result}
            else:
                raise TypeError(f"Unexpected node type: {type(updated_node)}")

        LOGGER.debug("Sending update for nodeid %s", updated_node.nodeid)
        self._socketio.emit("update", parents_slice)


def _run_test(nodeid: str, queue: multiprocessing.Queue, root_dir: str, test_dir: str):
    full_path = _get_full_path(nodeid, root_dir, test_dir)
    LOGGER.debug("full_path: %s", full_path)
    plugin = TestRunPlugin(queue=queue)
    pytest.main([full_path], plugins=[plugin])
    queue.put(_DONE)


def _get_full_path(nodeid: str, root_dir: str, test_dir: str) -> str:
    if not nodeid:
        return test_dir
    return nodeid.replace("/", os.sep)


class EnvironmentManager:

    COMPOSE_FILENAME = "docker_compose.yml"

    def __init__(self, directory: str, enable: bool):
        self._compose_path = os.path.join(directory, self.COMPOSE_FILENAME)
        self._proc = None
        self._enable = enable

    def __enter__(self):
        if self._enable and os.path.exists(self._compose_path):
            self._proc = subprocess.Popen(
                ["docker-compose", "-f", self._compose_path, "up"]
            )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._proc:
            subprocess.check_call(["docker-compose", "-f", self._compose_path, "down"])
            self._proc.wait()


def _init_result_tree(
    directory: str,
) -> Tuple[result_tree.BranchNode, Dict[str, result_tree.Node]]:
    """Collect the tests and initialise the result tree skeleton."""
    node, index = _init_result_tree_recur(directory)
    for child_branch in node.child_branches.values():
        result_tree.set_parent_ids(child_branch)
    return node, index


def _init_result_tree_recur(
    directory: str,
) -> Tuple[result_tree.BranchNode, Dict[str, result_tree.Node]]:
    root_node = result_tree.BranchNode(
        nodeid=directory.replace(os.sep, "/"),
        fspath=directory,
        short_id=os.path.basename(directory),
    )
    nodes_index: Dict[str, result_tree.Node] = {root_node.nodeid: root_node}

    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file() and entry.name.endswith(".py"):
                plugin = CollectPlugin()
                ret = pytest.main(["--collect-only", entry.path], plugins=[plugin])
                if ret != 0:
                    raise RuntimeError(f"Failed to collect tests from {entry.path}")

                session = plugin.session
                node, index = result_tree.build_from_session(session, entry.path)
            elif entry.is_dir():
                node, index = _init_result_tree_recur(entry.path)
            else:
                continue

            if list(node.iter_children()):
                root_node.child_branches[node.short_id] = node
                nodes_index.update(index)

    return root_node, nodes_index


class CollectPlugin:
    """PyTest plugin used to retrieve session object after collection."""

    def __init__(self):
        self.session = None

    def pytest_collection_finish(self, session):
        self.session = session


class TestRunPlugin:
    """PyTest plugin used to run tests and store results in our tree."""

    def __init__(self, queue=multiprocessing.Queue):
        self._queue = queue

    def pytest_runtest_logreport(self, report):
        """
        Hook called after a new test report is ready. Also called for
        setup/teardown.
        """
        # Currently do nothing for setup/teardown.
        if report.when != "call":
            return
        self._queue.put(report)
