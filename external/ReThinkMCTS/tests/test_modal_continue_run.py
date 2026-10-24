from __future__ import annotations

import unittest
import threading

from tools.modal_mcts import continue_run


class ContinueRunTests(unittest.TestCase):
    def test_failed_problem_replaced_while_other_workers_busy(self):
        slow_release = threading.Event()
        replacement_started = threading.Event()
        active = 0
        peak = 0
        lock = threading.Lock()
        recorded = []

        def run_one(position, dataset, key):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            if key == "slow":
                self.assertTrue(slow_release.wait(2))
            if key == "replacement":
                replacement_started.set()
                slow_release.set()
            with lock:
                active -= 1
            return {"status": "timeout" if key == "failed" else "completed"}

        continue_run.run_queue(
            [("apps", key) for key in ("slow", "failed", "replacement")], 2,
            run_one, lambda position, dataset, key, result: recorded.append((key, result["status"])),
        )
        self.assertTrue(replacement_started.is_set())
        self.assertEqual(peak, 2)
        self.assertIn(("failed", "timeout"), recorded)
        self.assertIn(("replacement", "completed"), recorded)

    def test_three_failures_still_dispatch_later_problems(self):
        recorded = []
        pending = [("apps", str(number)) for number in range(6)]

        def run_one(position, dataset, key):
            return {"status": "timeout" if int(key) < 3 else "completed"}

        continue_run.run_queue(
            pending, 4, run_one,
            lambda position, dataset, key, result: recorded.append((key, result["status"])),
        )
        self.assertEqual(len(recorded), 6)
        self.assertIn(("5", "completed"), recorded)


if __name__ == "__main__":
    unittest.main()
