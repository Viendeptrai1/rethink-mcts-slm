"""
CLI acceptance interface for RethinkMCTS matching §14 of spec.
Entry point: `rethink <subcommand>`
"""

import sys
import os
import json
import argparse
import logging
from rich.console import Console
from rich.table import Table

from rethink_mcts.config import AppConfig
from rethink_mcts.bootstrap import create_search_engine, create_solver
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    FunctionCase,
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.adapters.execution.docker_executor import DockerExecutor
from rethink_mcts.application.judge import HiddenJudge
from rethink_mcts.application.report import MetricsReporter

console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


from rethink_mcts.adapters.datasets.jsonl import parse_case_dict


def load_public_problem_from_file(path: str) -> PublicProblem:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

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


def load_hidden_problem_from_file(path: str) -> HiddenProblem:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    suite_data = data.get("hidden_suite", {})
    cases = [parse_case_dict(c) for c in suite_data.get("cases", [])]
    gen_cases = [parse_case_dict(c) for c in suite_data.get("generated_cases", [])]
    return HiddenProblem(
        problem_id=data["problem_id"],
        hidden_suite=HiddenSuite(
            cases=tuple(cases),
            suite_id=suite_data.get("suite_id", "hidden"),
            generated_cases=tuple(gen_cases)
        ),
        judge_spec=JudgeSpec(**data.get("judge_spec", {}))
    )


def cmd_doctor(args):
    console.print(f"[bold cyan]RethinkMCTS Doctor Check[/bold cyan]")
    console.print(f"Config: {args.config}")
    try:
        cfg = AppConfig.from_yaml_file(args.config)
        console.print("[green]✓ Config syntax and schema validation passed[/green]")
        console.print(f"  Model Transport: [yellow]{cfg.model.transport}[/yellow]")
        console.print(f"  Base URL: [yellow]{cfg.model.base_url}[/yellow]")
        console.print(f"  Model Name: [yellow]{cfg.model.model}[/yellow]")
        console.print(f"  Execution Backend: [yellow]{cfg.execution.backend}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]✗ Config validation failed:[/bold red] {e}")
        sys.exit(2)

    # Check model connectivity
    if cfg.model.transport == "openai_compatible":
        try:
            import requests
            resp = requests.get(f"{cfg.model.base_url}/models", timeout=1.5)
            if resp.status_code == 200:
                console.print(f"[green]✓ Endpoint {cfg.model.base_url} reachable (status 200)[/green]")
                models_data = resp.json().get("data", [])
                model_ids = [m.get("id") for m in models_data if isinstance(m, dict)]
                if cfg.model.model in model_ids:
                    console.print(f"[green]✓ Model '{cfg.model.model}' confirmed available on endpoint[/green]")
                else:
                    console.print(f"[yellow]! Model '{cfg.model.model}' not listed in /models (direct completion may still work)[/yellow]")
            else:
                console.print(f"[yellow]! Endpoint returned HTTP {resp.status_code} on /models[/yellow]")
        except Exception as e:
            console.print(f"[yellow]! Model endpoint offline or unreachable at {cfg.model.base_url} ({e.__class__.__name__})[/yellow]")
    elif cfg.model.transport == "mock":
        console.print("[green]✓ Mock scenario gateway ready[/green]")

    # Check executor
    if cfg.execution.backend == "docker":
        import shutil
        if shutil.which("docker"):
            console.print("[green]✓ Docker binary detected in PATH[/green]")
        else:
            console.print("[yellow]! Docker binary not found in PATH[/yellow]")
    else:
        executor = TrustedFixtureExecutor()
        tc = StdinCase(stdin="42\n", expected_stdout="42\n", case_id="doctor_probe")
        candidate = ProgramCandidate(
            candidate_id="probe",
            problem_id="doctor",
            code="print(input())",
            code_hash=ProgramCandidate.compute_hash("print(input())")
        )
        summary = executor.evaluate(
            candidate,
            tests=(tc,),
            spec=ExecutionSpec(mode="stdin"),
            limits=ProblemLimits(timeout_seconds=2.0)
        )
        if summary.all_passed:
            console.print("[green]✓ Trusted fixture executor verified (worker probe passed)[/green]")
        else:
            console.print(f"[red]✗ Worker probe failed[/red]")

    console.print("[bold green]System check completed successfully.[/bold green]")


def cmd_solve(args):
    solver_type = getattr(args, "solver", "mcts").lower()
    samples_n = getattr(args, "samples_n", 4)
    console.print(f"[bold cyan]Starting RethinkMCTS Solver [{solver_type.upper()}][/bold cyan]")
    cfg = AppConfig.from_yaml_file(args.config)

    # Override CLI options if provided
    if getattr(args, "endpoint", None):
        cfg.model.base_url = args.endpoint
    if getattr(args, "model", None):
        cfg.model.model = args.model

    problem = load_public_problem_from_file(args.problem)
    run_dir = args.output_dir or os.path.join(cfg.storage.output_dir, problem.problem_id)
    os.makedirs(run_dir, exist_ok=True)

    solver, store = create_solver(cfg, solver_type=solver_type, run_dir=run_dir, n=samples_n)
    console.print(f"Problem: [bold]{problem.problem_id}[/bold] ({len(problem.public_tests)} public tests)")

    result = solver.solve(problem)

    for cand, eval_rec in result.archive.entries:
        store.save_candidate(cand)
        store.save_evaluation(eval_rec)

    if result.selected_candidate:
        store.save_selected_candidate(problem.problem_id, result.selected_candidate)
        console.print(f"[bold green]✓ Search Complete![/bold green]")
        console.print(f"  Best Public Reward: [yellow]{result.best_reward:.3f}[/yellow]")
        console.print(f"  Stop Reason: {result.stop_reason}")
        console.print(f"  Selected Code saved to: [cyan]{run_dir}/problems/{problem.problem_id}/selected.py[/cyan]")
    else:
        console.print("[bold red]✗ No valid candidate solution found.[/bold red]")
        sys.exit(4)

    store.save_usage(result.usage)
    console.print(f"  Total Model Calls: {result.usage.total_model_calls}")
    console.print(f"  Code Generations: {result.usage.code_generation_attempts}")
    console.print(f"  Rethink Attempts: {result.usage.rethink_attempts}")


def cmd_judge(args):
    console.print(f"[bold cyan]Running Independent Hidden Judge[/bold cyan]")
    hidden_problem = load_hidden_problem_from_file(args.hidden)

    # Load frozen candidate
    selected_py = os.path.join(args.run, "problems", hidden_problem.problem_id, "selected.py")
    if not os.path.exists(selected_py):
        # Check direct path
        selected_py = os.path.join(args.run, "selected.py")
    if not os.path.exists(selected_py):
        console.print(f"[bold red]Selected program not found in run dir: {args.run}[/bold red]")
        sys.exit(2)

    with open(selected_py, "r", encoding="utf-8") as f:
        code = f.read()

    candidate = ProgramCandidate(
        candidate_id="frozen_selected",
        problem_id=hidden_problem.problem_id,
        code=code,
        code_hash=ProgramCandidate.compute_hash(code)
    )

    executor = TrustedFixtureExecutor()
    judge = HiddenJudge(executor=executor)
    result = judge.judge(candidate, hidden_problem)

    judge_file = os.path.join(args.run, "judge_results.json")
    with open(judge_file, "w", encoding="utf-8") as f:
        json.dump({
            "problem_id": result.problem_id,
            "candidate_id": result.candidate_id,
            "code_hash": result.code_hash,
            "all_hidden_passed": result.all_hidden_passed,
            "hidden_pass_rate": result.hidden_pass_rate,
            "hidden_passed": result.hidden_passed,
            "hidden_total": result.hidden_total
        }, f, indent=2)

    console.print(f"[bold]Judge Evaluation Complete:[/bold]")
    console.print(f"  Passed: {result.hidden_passed}/{result.hidden_total} ({result.hidden_pass_rate*100:.1f}%)")
    if result.all_hidden_passed:
        console.print("[bold green]✓ 100% Hidden Tests ACCEPTED[/bold green]")
    else:
        console.print("[bold yellow]! Candidate failed some hidden tests[/bold yellow]")


def cmd_report(args):
    reporter = MetricsReporter(run_dir=args.run)
    rep = reporter.generate_report()
    console.print(f"[bold cyan]Summary Report for {args.run}:[/bold cyan]")
    console.print(f"  Public Best Reward: {rep['public_evaluation']['best_public_reward']}")
    console.print(f"  Selected Solution Pass@1: {rep['hidden_evaluation']['selected_solution_pass_at_1']}%")
    console.print(f"  Report written to: [green]{args.run}/reports/summary.md[/green]")


def cmd_prepare(args):
    console.print(f"[bold cyan]Preparing Dataset: {args.dataset}[/bold cyan]")
    from rethink_mcts.application.prepare import prepare_dataset
    manifest = prepare_dataset(
        dataset_name=args.dataset,
        raw_path=args.raw_path,
        output_dir=args.output,
        limit=args.limit
    )
    console.print(f"[bold green]✓ Prepared {manifest['total_problems']} problems[/bold green]")
    console.print(f"  Public problems: [cyan]{manifest['public_problems_path']}[/cyan]")
    console.print(f"  Judge suites dir: [cyan]{manifest['judge_suites_dir']}[/cyan]")


def main():
    parser = argparse.ArgumentParser(description="RethinkMCTS CLI acceptance interface")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # prepare
    p_prep = subparsers.add_parser("prepare", help="Prepare dataset into separated public and judge stores")
    p_prep.add_argument("--dataset", type=str, required=True, choices=["humaneval", "apps", "code_contests"], help="Dataset name")
    p_prep.add_argument("--raw-path", type=str, default=None, help="Path to raw source file (optional)")
    p_prep.add_argument("--output", type=str, default=None, help="Output directory (default: prepared/<dataset>)")
    p_prep.add_argument("--limit", type=int, default=None, help="Maximum problems to prepare")

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Check config, model connectivity, and sandbox")
    p_doc.add_argument("--config", type=str, default="configs/smoke_mock.yaml", help="Path to config YAML")

    # solve
    p_solve = subparsers.add_parser("solve", help="Run solver (MCTS or Baseline) on public problem")
    p_solve.add_argument("--config", type=str, required=True, help="Path to config YAML")
    p_solve.add_argument("--problem", type=str, required=True, help="Path to public problem JSON")
    p_solve.add_argument("--solver", type=str, default="mcts", choices=["mcts", "direct", "best_of_n", "graph"], help="Solver method: mcts (default), direct, best_of_n, or graph")
    p_solve.add_argument("--samples-n", type=int, default=4, help="Number of candidate samples for best_of_n solver (default: 4)")
    p_solve.add_argument("--output-dir", type=str, default=None, help="Output directory for run artifacts")
    p_solve.add_argument("--endpoint", type=str, default=None, help="Override endpoint URL")
    p_solve.add_argument("--model", type=str, default=None, help="Override model name")

    # judge
    p_judge = subparsers.add_parser("judge", help="Evaluate frozen candidate on hidden suite")
    p_judge.add_argument("--run", type=str, required=True, help="Path to run directory")
    p_judge.add_argument("--hidden", type=str, required=True, help="Path to hidden suite JSON")

    # report
    p_rep = subparsers.add_parser("report", help="Generate summary report for a run")
    p_rep.add_argument("--run", type=str, required=True, help="Path to run directory")

    args = parser.parse_args()

    if args.subcommand == "prepare":
        cmd_prepare(args)
    elif args.subcommand == "doctor":
        cmd_doctor(args)
    elif args.subcommand == "solve":
        cmd_solve(args)
    elif args.subcommand == "judge":
        cmd_judge(args)
    elif args.subcommand == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
