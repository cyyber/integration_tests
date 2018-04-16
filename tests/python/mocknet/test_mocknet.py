# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
from unittest import TestCase

from mocknet.mocknet import MockNet


class TestMocknetHelpers(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_timeout(self):
        def func_blocks():
            while mocknet.running:
                time.sleep(1)

        mocknet = MockNet(func_blocks,
                          timeout_secs=2,
                          node_count=0)
        with self.assertRaises(TimeoutError):
            mocknet.run()

    def test_exception(self):
        def func_raises_value_error():
            time.sleep(1)
            raise ValueError("Some random exception")

        mocknet = MockNet(func_raises_value_error,
                          timeout_secs=10,
                          node_count=0)

        with self.assertRaises(ValueError):
            mocknet.run()

    def test_works_ok(self):
        def func_no_issues():
            time.sleep(1)
            print("OK - NodeCount %d" % mocknet.node_count)

        mocknet = MockNet(func_no_issues,
                          timeout_secs=10,
                          node_count=0)
        mocknet.run()

    def test_launch_1_node(self):
        def func_monitor_log():
            running_time = 5
            start = time.time()
            while time.time() - start < running_time:
                try:
                    msg = mocknet.log_queue.get(False)
                    print(msg, end='')
                except Exception as e:  # noqa
                    time.sleep(0.1)

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=10,
                          node_count=1)
        mocknet.prepare_source()
        mocknet.run()

    def test_launch_log_nodes(self):
        def func_monitor_log():
            running_time = 10
            start = time.time()
            while time.time() - start < running_time:
                try:
                    msg = mocknet.log_queue.get(False)
                    print(msg, end='')
                except Exception as e:  # noqa
                    time.sleep(0.1)

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=120,
                          node_count=10)
        mocknet.prepare_source()
        mocknet.run()