"""
Batch benchmark evaluation runner for RethinkMCTS.
Runs full evaluation across HumanEval (164 problems) or APPS (300 problems)
using specified solver (direct, best_of_n, mcts) on Modal vLLM server.

Supports:
- Automatic resume from checkpoint (skips already completed problems)
- Live metrics calculation (Pass@1, Pass Rate, Latency, Token accounting)
- Persistent Markdown and JSON summary updates after every problem
- Fault tolerance (catches per-problem exceptions and continues)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.table import Table

from rethink_mcts.config import AppConfig
from rethink_mcts.bootstrap import create_solver
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata
)
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.adapters.datasets.jsonl import parse_case_dict
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.adapters.execution.docker_executor import DockerExecutor
from rethink_mcts.application.judge import HiddenJudge
from rethink_mcts.cli import load_hidden_problem_from_file

console = Console()


def parse_public_problem(data: dict) -> PublicProblem:
    public_tests = [parse_case_dict(c) for c in data.get("public_tests", [])]
    spec_data = data.get("execution_spec", {})
    return PublicProblem(
        problem_id=data["problem_id"],
        statement=data["statement"],
        execution_spec=ExecutionSpec(
            mode=spec_data.get("mode", "stdin"),
            entry_point=spec_data.get("entry_point")
        ),
        public_tests=tuple(public_tests),
        limits=ProblemLimits(**data.get("limits", {})),
        metadata=PublicMetadata(**data.get("metadata", {}))
    )


def run_batch(
    config_path: str,
    dataset: str,
    solver_name: str,
    output_dir: str,
    samples_n: int = 3,
    limit: Optional[int] = None,
    resume: bool = True,
    problem_ids: Optional[List[str]] = None,
    difficulty: Optional[str] = None
):
    console.print(f"[bold cyan]============================================================[/bold cyan]")
    console.print(f"[bold cyan]RethinkMCTS Batch Benchmark Runner[/bold cyan]")
    console.print(f"Dataset: [yellow]{dataset}[/yellow]")
    console.print(f"Solver: [yellow]{solver_name.upper()}[/yellow]" + (f" (N={samples_n})" if solver_name == "best_of_n" else ""))
    console.print(f"Config: [yellow]{config_path}[/yellow]")
    console.print(f"Output: [yellow]{output_dir}[/yellow]")
    if difficulty:
        console.print(f"Filtered by Difficulty: [yellow]{difficulty}[/yellow]")
    if problem_ids:
        console.print(f"Filtered to [yellow]{len(problem_ids)}[/yellow] specific problem IDs")
    console.print(f"[bold cyan]============================================================[/bold cyan]")

    cfg = AppConfig.from_yaml_file(config_path)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Locate manifest and problem files
    manifest_path = f"prepared/{dataset}/manifest.json"
    if not os.path.exists(manifest_path):
        console.print(f"[bold red]Manifest not found at {manifest_path}[/bold red]")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    public_path = manifest["public_problems_path"]
    suites_dir = manifest["judge_suites_dir"]

    # Read all public problems
    problems: List[PublicProblem] = []
    with open(public_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                p = parse_public_problem(json.loads(line.strip()))
                if difficulty and getattr(p.metadata, "difficulty", None) != difficulty:
                    continue
                if problem_ids is None or p.problem_id in problem_ids:
                    problems.append(p)

    if limit and limit > 0:
        problems = problems[:limit]

    total_problems = len(problems)
    console.print(f"Loaded [green]{total_problems}[/green] problems to evaluate.")

    # 2. Select execution backend
    if cfg.execution.backend == "docker":
        executor = DockerExecutor(allow_host_fallback=True)
    else:
        executor = TrustedFixtureExecutor()
    judge = HiddenJudge(executor=executor)

    # 3. Track metrics
    completed_problems = 0
    passed_hidden_count = 0
    total_model_calls = 0
    total_code_gens = 0
    total_rethink_attempts = 0
    total_elapsed_seconds = 0.0
    results_list: List[Dict[str, Any]] = []

    start_batch_time = time.time()

    for idx, problem in enumerate(problems, start=1):
        prob_id = problem.problem_id
        prob_dir = os.path.join(output_dir, "problems", prob_id)
        judge_file = os.path.join(prob_dir, "judge_results.json")
        selected_file = os.path.join(prob_dir, "selected.py")
        usage_file = os.path.join(prob_dir, "usage.json")

        suite_path = os.path.join(suites_dir, f"{prob_id}.json")
        if not os.path.exists(suite_path):
            console.print(f"[{idx}/{total_problems}] [red]Missing hidden suite for {prob_id}[/red]")
            continue

        hidden_problem = load_hidden_problem_from_file(suite_path)

        # Check resume
        if resume and os.path.exists(judge_file) and os.path.exists(selected_file):
            with open(judge_file, "r", encoding="utf-8") as f:
                jdata = json.load(f)
            udata = {}
            if os.path.exists(usage_file):
                with open(usage_file, "r", encoding="utf-8") as f:
                    udata = json.load(f)

            is_pass = jdata.get("all_hidden_passed", False)
            completed_problems += 1
            if is_pass:
                passed_hidden_count += 1
            total_model_calls += udata.get("total_model_calls", 0)
            total_code_gens += udata.get("code_generation_attempts", 0)
            total_rethink_attempts += udata.get("rethink_attempts", 0)

            results_list.append({
                "problem_id": prob_id,
                "passed": is_pass,
                "hidden_pass_rate": jdata.get("hidden_pass_rate", 0.0),
                "model_calls": udata.get("total_model_calls", 0),
                "wall_time": udata.get("wall_time_seconds", 0.0),
                "resumed": True
            })

            curr_pass_at_1 = (passed_hidden_count / completed_problems) * 100.0
            verdict_str = "[green]PASS[/green]" if is_pass else "[red]FAIL[/red]"
            console.print(f"[{idx}/{total_problems}] [dim]Resumed[/dim] {prob_id} -> {verdict_str} | Running Pass@1: [bold]{curr_pass_at_1:.1f}%[/bold] ({passed_hidden_count}/{completed_problems})")
            continue

        # Solve problem
        os.makedirs(prob_dir, exist_ok=True)
        prob_start = time.time()
        is_pass = False
        hidden_pass_rate = 0.0
        p_model_calls = 0
        p_code_gens = 0
        p_rethinks = 0

        try:
            solver, store = create_solver(
                cfg,
                solver_type=solver_name,
                run_dir=output_dir,
                n=samples_n
            )
            result = solver.solve(problem)

            for cand, eval_rec in result.archive.entries:
                store.save_candidate(cand)
                store.save_evaluation(eval_rec)

            if result.selected_candidate:
                store.save_selected_candidate(prob_id, result.selected_candidate)
                # Judge hidden
                j_res = judge.judge(result.selected_candidate, hidden_problem)
                is_pass = j_res.all_hidden_passed
                hidden_pass_rate = j_res.hidden_pass_rate

                with open(judge_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "problem_id": prob_id,
                        "candidate_id": j_res.candidate_id,
                        "code_hash": j_res.code_hash,
                        "all_hidden_passed": j_res.all_hidden_passed,
                        "hidden_pass_rate": j_res.hidden_pass_rate,
                        "hidden_passed": j_res.hidden_passed,
                        "hidden_total": j_res.hidden_total
                    }, f, indent=2)

            p_model_calls = result.usage.total_model_calls
            p_code_gens = result.usage.code_generation_attempts
            p_rethinks = result.usage.rethink_attempts

        except Exception as e:
            console.print(f"[{idx}/{total_problems}] [bold red]Error solving {prob_id}:[/bold red] {e}")
            with open(judge_file, "w", encoding="utf-8") as f:
                json.dump({
                    "problem_id": prob_id,
                    "all_hidden_passed": False,
                    "hidden_pass_rate": 0.0,
                    "error": str(e)
                }, f, indent=2)

        prob_elapsed = time.time() - prob_start
        # Save per-problem usage
        with open(usage_file, "w", encoding="utf-8") as f:
            json.dump({
                "problem_id": prob_id,
                "total_model_calls": p_model_calls,
                "code_generation_attempts": p_code_gens,
                "rethink_attempts": p_rethinks,
                "wall_time_seconds": round(prob_elapsed, 2)
            }, f, indent=2)
        total_elapsed_seconds += prob_elapsed
        completed_problems += 1
        if is_pass:
            passed_hidden_count += 1
        total_model_calls += p_model_calls
        total_code_gens += p_code_gens
        total_rethink_attempts += p_rethinks

        results_list.append({
            "problem_id": prob_id,
            "passed": is_pass,
            "hidden_pass_rate": hidden_pass_rate,
            "model_calls": p_model_calls,
            "wall_time": round(prob_elapsed, 2),
            "resumed": False
        })

        curr_pass_at_1 = (passed_hidden_count / completed_problems) * 100.0
        verdict_str = "[bold green]PASS[/bold green]" if is_pass else "[bold red]FAIL[/bold red]"
        console.print(f"[{idx}/{total_problems}] {prob_id} -> {verdict_str} | Running Pass@1: [bold yellow]{curr_pass_at_1:.1f}%[/bold yellow] ({passed_hidden_count}/{completed_problems}) | Time: {prob_elapsed:.1f}s")

        # Live summary update
        write_summary(output_dir, dataset, solver_name, samples_n, results_list, total_problems, start_batch_time)

    console.print(f"\n[bold green]============================================================[/bold green]")
    console.print(f"[bold green]Batch Benchmark Complete![/bold green]")
    final_pass_rate = (passed_hidden_count / completed_problems * 100.0) if completed_problems else 0.0
    console.print(f"Total Evaluated: {completed_problems}/{total_problems}")
    console.print(f"Final Pass@1: [bold yellow]{final_pass_rate:.2f}%[/bold yellow] ({passed_hidden_count}/{completed_problems})")
    console.print(f"Total Model Calls: {total_model_calls}")
    console.print(f"Total Time: {time.time() - start_batch_time:.1f}s")
    console.print(f"Reports saved to: [cyan]{output_dir}/summary.md[/cyan]")
    console.print(f"[bold green]============================================================[/bold green]")


def write_summary(
    output_dir: str,
    dataset: str,
    solver_name: str,
    samples_n: int,
    results: List[Dict[str, Any]],
    total_expected: int,
    start_time: float
):
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    pass_at_1 = (passed / total * 100.0) if total else 0.0
    mean_pass_rate = (sum(r.get("hidden_pass_rate", 0.0) for r in results) / total * 100.0) if total else 0.0
    total_calls = sum(r.get("model_calls", 0) for r in results)
    elapsed = time.time() - start_time

    summary_data = {
        "dataset": dataset,
        "solver": solver_name,
        "samples_n": samples_n if solver_name == "best_of_n" else None,
        "evaluated_problems": total,
        "total_expected_problems": total_expected,
        "passed_problems": passed,
        "pass_at_1_percent": round(pass_at_1, 2),
        "mean_hidden_pass_rate_percent": round(mean_pass_rate, 2),
        "total_model_calls": total_calls,
        "elapsed_seconds": round(elapsed, 1),
        "results": results
    }

    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    md_lines = [
        f"# Benchmark Results: {dataset.upper()} - {solver_name.upper()}",
        "",
        f"- **Dataset**: `{dataset}` ({total}/{total_expected} problems evaluated)",
        f"- **Solver**: `{solver_name}`" + (f" (N={samples_n})" if solver_name == "best_of_n" else ""),
        f"- **Selected Solution Pass@1**: **{pass_at_1:.2f}%** ({passed}/{total})",
        f"- **Mean Hidden Pass Rate**: **{mean_pass_rate:.2f}%**",
        f"- **Total Model Calls**: {total_calls}",
        f"- **Total Elapsed Time**: {elapsed:.1f}s",
        "",
        "## Per-Problem Breakdown",
        "",
        "| Problem ID | Verdict | Hidden Pass Rate | Calls | Time (s) | Resumed |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for r in results:
        v = "✅ PASS" if r.get("passed") else "❌ FAIL"
        hpr = f"{r.get('hidden_pass_rate', 0.0)*100:.1f}%"
        res = "Yes" if r.get("resumed") else "No"
        md_lines.append(f"| `{r['problem_id']}` | {v} | {hpr} | {r.get('model_calls', 0)} | {r.get('wall_time', 0.0)}s | {res} |")

    with open(os.path.join(output_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch benchmark evaluation runner for RethinkMCTS")
    parser.add_argument("--config", default="configs/modal_14b.yaml", help="Path to config YAML")
    parser.add_argument("--dataset", default="humaneval", choices=["humaneval", "apps"], help="Dataset to evaluate")
    parser.add_argument("--solver", default="direct", choices=["direct", "best_of_n", "mcts", "graph"], help="Solver method")
    parser.add_argument("--samples-n", type=int, default=3, help="Number of samples for best_of_n")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: runs/<dataset>_<solver>_14b)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of problems")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume from existing files")
    parser.add_argument("--problem-ids", type=str, default=None, help="Comma-separated problem IDs to evaluate (e.g. python_50,python_65)")
    parser.add_argument("--difficulty", type=str, default=None, choices=["introductory", "interview", "competition"], help="Filter by difficulty level for APPS")

    args = parser.parse_args()
    diff_suffix = f"_{args.difficulty}" if args.difficulty else ""
    out_dir = args.output_dir or f"runs/{args.dataset}_{args.solver}{diff_suffix}_14b"
    p_ids = [pid.strip() for pid in args.problem_ids.split(",") if pid.strip()] if args.problem_ids else None

    run_batch(
        config_path=args.config,
        dataset=args.dataset,
        solver_name=args.solver,
        output_dir=out_dir,
        samples_n=args.samples_n,
        limit=args.limit,
        resume=not args.no_resume,
        problem_ids=p_ids,
        difficulty=args.difficulty
    )


