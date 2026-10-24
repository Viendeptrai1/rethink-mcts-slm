from __future__ import annotations

import hashlib
import unittest

from baselines.sample_selection import load_sample_manifest
from evaluation.benchmark_judge import DEFAULT_APPS_SAMPLE, DEFAULT_HUMANEVAL_SAMPLE


class BenchmarkCohortTests(unittest.TestCase):
    def test_apps_matches_frozen_peer_cohort(self) -> None:
        manifest = load_sample_manifest(DEFAULT_APPS_SAMPLE, dataset="apps")
        ids = manifest["problem_ids"]
        difficulty = manifest["difficulty_by_problem_id"]
        self.assertEqual(len(ids), 300)
        self.assertEqual(len(set(ids)), 300)
        self.assertEqual(
            {name: list(difficulty.values()).count(name) for name in ("introductory", "interview", "competition")},
            {"introductory": 100, "interview": 100, "competition": 100},
        )
        cohort_csv = ",".join(f"apps_{problem_id}" for problem_id in ids)
        self.assertEqual(
            hashlib.sha256(cohort_csv.encode("ascii")).hexdigest(),
            "badce36e72a9822ec6e1b8becd2847dfb26b850883adba7dce253317e647c0c9",
        )

    def test_humaneval_is_entire_test_split(self) -> None:
        manifest = load_sample_manifest(DEFAULT_HUMANEVAL_SAMPLE, dataset="humaneval")
        self.assertEqual(manifest["problem_ids"], list(range(164)))


if __name__ == "__main__":
    unittest.main()
