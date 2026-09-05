"""
Reporting and metrics aggregation service matching §15.2 of RethinkMCTS spec.
"""

import os
import json
from typing import Dict, Any, Optional


class MetricsReporter:
    def __init__(self, run_dir: str):
        self.run_dir = run_dir

    def generate_report(self) -> Dict[str, Any]:
        usage_path = os.path.join(self.run_dir, "usage.json")
        usage_data = {}
        if os.path.exists(usage_path):
            with open(usage_path, "r", encoding="utf-8") as f:
                usage_data = json.load(f)

        judge_path = os.path.join(self.run_dir, "judge_results.json")
        judge_data = {}
        if os.path.exists(judge_path):
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)

        evals_path = os.path.join(self.run_dir, "evaluations.jsonl")
        evaluations = []
        if os.path.exists(evals_path):
            with open(evals_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        evaluations.append(json.loads(line.strip()))

        # Calculate metrics
        public_all_passed = any(e.get("all_passed") for e in evaluations)
        best_public_reward = max((e.get("reward", 0.0) or 0.0 for e in evaluations), default=0.0)

        report = {
            "run_dir": self.run_dir,
            "public_evaluation": {
                "total_evaluations": len(evaluations),
                "public_all_passed": public_all_passed,
                "best_public_reward": round(best_public_reward, 3)
            },
            "hidden_evaluation": {
                "judged": bool(judge_data),
                "selected_solution_pass_at_1": 100.0 if judge_data.get("all_hidden_passed") else 0.0,
                "hidden_pass_rate": round(judge_data.get("hidden_pass_rate", 0.0) * 100.0, 1),
                "hidden_passed": judge_data.get("hidden_passed", 0),
                "hidden_total": judge_data.get("hidden_total", 0)
            },
            "usage": usage_data
        }

        # Write reports
        reports_dir = os.path.join(self.run_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)

        with open(os.path.join(reports_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        md_content = f"""# RethinkMCTS Experiment Summary

- **Run Directory**: `{self.run_dir}`
- **Public Best Reward**: {best_public_reward:.3f}
- **Selected Solution Pass@1**: {report['hidden_evaluation']['selected_solution_pass_at_1']}%
- **Mean Hidden Pass Rate**: {report['hidden_evaluation']['hidden_pass_rate']}%

## Compute & Search Accounting
- **Total Model Calls**: {usage_data.get('total_model_calls', 0)}
- **Code Generation Attempts**: {usage_data.get('code_generation_attempts', 0)}
- **Rethink Attempts**: {usage_data.get('rethink_attempts', 0)}
- **Total Tokens**: {usage_data.get('total_tokens', 0)}
- **Wall Time**: {usage_data.get('wall_time_seconds', 0.0)}s
"""
        with open(os.path.join(reports_dir, "summary.md"), "w", encoding="utf-8") as f:
            f.write(md_content)

        return report
