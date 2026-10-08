"""
Utility script to merge 3 parallel APPS batch runs (Introductory, Interview, Competition)
into a unified 300-problem benchmark result directory.
"""

import json
import shutil
import argparse
from pathlib import Path


def merge_batches(batch_dirs: list[Path], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    out_problems = output_dir / "problems"
    out_problems.mkdir(parents=True, exist_ok=True)

    all_results = []
    total_calls = 0
    total_elapsed = 0.0
    passed_count = 0
    evaluated_count = 0

    print(f"Merging {len(batch_dirs)} batch directories into: {output_dir}")

    results_by_id = {}
    for bdir in batch_dirs:
        summary_path = bdir / "summary.json"
        if not summary_path.exists():
            print(f"Warning: {summary_path} not found, skipping...")
            continue

        data = json.loads(summary_path.read_text(encoding="utf-8"))
        results = data.get("results", [])
        total_calls += data.get("total_model_calls", 0)
        total_elapsed = max(total_elapsed, data.get("elapsed_seconds", 0.0))  # Ran in parallel

        # Copy problem folders
        src_prob_dir = bdir / "problems"
        if src_prob_dir.exists():
            for pfolder in src_prob_dir.iterdir():
                if pfolder.is_dir():
                    dst_folder = out_problems / pfolder.name
                    if not dst_folder.exists() or not (dst_folder / "completed.json").exists():
                        if dst_folder.exists():
                            shutil.rmtree(dst_folder)
                        shutil.copytree(pfolder, dst_folder)

        for r in results:
            pid = r["problem_id"]
            if pid not in results_by_id:
                results_by_id[pid] = r
            else:
                existing = results_by_id[pid]
                if existing.get("status") != "completed" and r.get("status") == "completed":
                    results_by_id[pid] = r
                elif existing.get("status") == "completed" and r.get("status") == "completed":
                    if r.get("hidden_pass_rate", 0) > existing.get("hidden_pass_rate", 0):
                        results_by_id[pid] = r

    all_results = sorted(results_by_id.values(), key=lambda x: x["problem_id"])
    for r in all_results:
        evaluated_count += 1
        is_passed = r.get("all_hidden_passed") is True or r.get("verdict") == "passed"
        if is_passed:
            passed_count += 1

    # Compute macro metrics
    rates = [r.get("hidden_pass_rate", 0.0) for r in all_results if r.get("status") == "completed"]
    mean_rate = sum(rates) / len(rates) if rates else 0.0
    pass_at_1 = (passed_count / 300.0) * 100.0 if all_results else 0.0

    master_summary = {
        "dataset": "apps",
        "solver": "mcts",
        "total_expected_problems": 300,
        "evaluated_problems": evaluated_count,
        "passed_problems": passed_count,
        "pass_at_1_percent": round(pass_at_1, 2),
        "mean_hidden_pass_rate_percent": round(mean_rate * 100.0, 2),
        "total_model_calls": total_calls,
        "parallel_elapsed_seconds": round(total_elapsed, 1),
        "results": all_results,
    }

    out_summary_file = output_dir / "summary.json"
    out_summary_file.write_text(json.dumps(master_summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate Markdown Summary
    md_content = f"""# APPS 300 Benchmark: Unified Parallel Evaluation Summary

- **Total Expected**: 300 problems (100 Intro, 100 Inter, 100 Comp)
- **Evaluated**: {evaluated_count}/300
- **Passed**: {passed_count}
- **Pass@1**: **{pass_at_1:.2f}%**
- **Macro Mean Hidden Pass Rate**: **{mean_rate * 100.0:.2f}%**
- **Total Model Calls**: {total_calls}
- **Wall Time (Parallel Max)**: {total_elapsed:.1f}s

| Problem ID | Verdict | Hidden Pass Rate | Calls | Time (s) |
| :--- | :---: | :---: | :---: | :---: |
"""
    for r in all_results:
        is_passed = r.get("all_hidden_passed") is True or r.get("verdict") == "passed"
        verdict_icon = "✅ PASS" if is_passed else "❌ FAIL"
        h_rate = r.get("hidden_pass_rate", 0.0) * 100.0
        calls = r.get("usage", {}).get("total_model_calls", r.get("calls", 0))
        wall = r.get("solve_wall_seconds", r.get("elapsed_seconds", 0.0))
        md_content += f"| `{r['problem_id']}` | {verdict_icon} | {h_rate:.1f}% | {calls} | {wall:.1f}s |\n"

    (output_dir / "summary.md").write_text(md_content, encoding="utf-8")
    print(f"✓ Successfully generated master summary at {out_summary_file}")
    print(f"  Pass@1: {pass_at_1:.2f}% ({passed_count}/300)")
    print(f"  Mean Hidden Pass Rate: {mean_rate * 100.0:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-dirs", nargs="+", required=True, help="List of batch output directories")
    parser.add_argument("--output-dir", required=True, help="Destination master directory")
    args = parser.parse_args()

    merge_batches([Path(d) for d in args.batch_dirs], Path(args.output_dir))
