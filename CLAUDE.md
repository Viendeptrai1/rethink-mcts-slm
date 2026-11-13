# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Thesis project (TLCN): a native re-implementation of **RethinkMCTS** (arXiv:2409.09584v2), thought-level MCTS for code generation with execution feedback. It is evaluated with **protocol v3.1** on several open 7–9B models (Qwen2.5-Coder-7B, Seed-Coder-8B, Qwen3.5-9B) on APPS-300 and HumanEval-164, against Direct and Best-of-16 baselines. The main package is `src/rethink_mcts/`. Runs execute on A100-SXM4-40GB via Colab (`deploy/colab/`) or Modal (`deploy/modal_v31_runner.py`). All pre-v3 material (14B v1 runs, the teammate's 7B branch in `external/`, old configs, scripts, summaries and report chapters) was removed from the branch on 13/11/2026 and is preserved at git tag `archive/pre-v3-2026-11-13`; do not cite it unless the user asks.

- Talk to the user in **Vietnamese**. Code, identifiers and short comments may be in English. All docs and the report are in Vietnamese.
- `CONTEXT_MANIFEST.md` maps each research concern to its source-of-truth file in `docs/research/` (CURRENT_STATE, DECISION_LOG, ROADMAP, RESEARCH_LOG, HYPOTHESIS_LAB, PROTOCOL). Read only the file the task needs, and update only the file whose concern changed. Never promote a hypothesis to a conclusion on your own.
- **The only source of benchmark numbers** is `docs/results/BENCHMARK_LEDGER.md` and `docs/results/v3/` (built from `runs/v3_*` with `scripts/analyze_v3.py`). `Proposal.md` is older material (its title still stands). The configs that exist live in `configs/`.
- The thesis report outline is `docs/report/KHUNG_BAO_CAO_v2.md` (chapters are to be rewritten from it). Every number in the report must link to a source artifact under `runs/v3_*` or `docs/results/`. Never mix results from different cohorts or protocols in one table.

## Commands

```bash
pip install -e ".[dev]"            # installs the `rethink` CLI; extras: datasets, serving (modal, openai)
python3 -m pytest -q               # pytest config sets pythonpath=src, so tests also run without installing
python3 -m pytest tests/unit/test_policies.py::test_name -q   # single test
```

Two tests need the Docker image `rethink-worker:py311` and fail without it: `tests/acceptance/test_scenario_c.py` and `tests/integration/test_research_foundation.py::test_docker_real_container_execution_and_trace`. Build the image with `docker build -t rethink-worker:py311 deploy/sandbox`. The other tests run offline.

CLI (`rethink <cmd>` or `python3 -m rethink_mcts.cli <cmd>`):

```bash
rethink doctor  --config configs/smoke_mock.yaml                  # validate config, probe endpoint and executor
rethink prepare --dataset apps --raw-path data/apps/apps_300.jsonl --output prepared/apps_half --public-split half
rethink solve   --config configs/smoke_mock.yaml --problem tests/fixtures/watermelon_public.json \
                --output-dir runs/smoke_demo [--solver mcts|direct|best_of_n|iterative_repair|graph]
rethink judge   --run runs/smoke_demo --hidden tests/fixtures/watermelon_hidden.json
rethink report  --run runs/smoke_demo
rethink benchmark --config configs/research_smoke.yaml --output-dir runs/x --dry-run   # no model calls, no writes
```

Multi-problem benchmark runs go through `scripts/run_benchmark_batch.py`. It wraps `application/benchmark.run_benchmark`, resumes by default (`--no-resume` turns that off), and accepts `--problem-ids @<cohort file>`, `--dataset`, `--difficulty`, `--limit`, `--workers N` (problems solved concurrently), `--dry-run` and repeated `--set section.field=value` overrides. v3.1 configs are in `configs/v3_7b/` (see its README). `scripts/pilot_report.py` and `scripts/pilot_gate.py` check run health; `scripts/analyze_v3.py` builds the paired analysis (McNemar + Holm, bootstrap, offline critic/early-stop and Best-of-k) used by the ledger.

## Cost and safety

- **Do not deploy or call Modal GPUs, or start any non-dry-run benchmark against a real endpoint, unless the user explicitly asks.** These runs spend real credit (Colab compute units or Modal credit). `deploy/modal_v31_runner.py` runs a whole plan in one Modal A100 container; `deploy/colab/` drives Colab A100 sessions through the `colab` CLI (see `deploy/colab/v31_campaign/README.md`); `scripts/modal_spending_guard.py` is a billing circuit breaker for Modal. For a first real run, keep the problem count and budget small.
- Validate with `--dry-run` or the `mock` transport (`configs/smoke_mock.yaml`, `configs/research_smoke.yaml`) first.
- `trusted_fixture` execution is a host subprocess, not a security sandbox. `docker` never falls back to host execution.
- Never run two processes that write to the same run output directory. Use a fresh directory per model × dataset × method × seed × budget.

## Architecture

Ports & adapters (hexagonal) layout inside `src/rethink_mcts/`:

- `domain/` holds pure entities with no external imports: `PublicProblem` vs `HiddenProblem`, the immutable `ProgramCandidate`, `Tree`/`SearchNode`/`ThoughtRevision`, budget/usage accounting, events and errors.
- `policies/` holds the paper formulas: P-UCB selection (`c`, `c_base`), Max/Mean backup, `PaperDualRewardPolicy` (the critic runs only when every public test passes), prior normalisation, stopping and final selection.
- `ports/` defines the abstract interfaces. `adapters/` implements them:
  - `llm/`: `HttpModelGateway` (OpenAI-compatible), `SemanticPromptedLLM` (renders the Jinja prompts in `prompts/<bundle>/` and implements propose/generate/refine/assess/analyze), `ScenarioMockLLM`.
  - `execution/`: trusted-fixture and Docker executors, shared harnesses and comparators, bytecode CFG plus dynamic tracing in a separate worker.
  - `datasets/` and `storage/`.
- `application/` orchestrates the use cases: `SearchEngine` (MCTS loop with leaf revision), `CandidateEvaluator` (public tests plus reward), `FeedbackService` (feedback modes `none|facts_only|trace|block|adaptive`; adaptive escalates after `escalate_after` attempts that show no improvement), the baselines (`DirectBaseline`, `BestOfNPublicBaseline`, `IterativeRepairBaseline`), the exploratory `GraphSolver`, `HiddenJudge`, and `benchmark.py`.
- `bootstrap.create_solver` is the **only** place that wires dependencies from config. Add a new solver, policy or backend there and in `config.py`. Do not construct objects ad hoc elsewhere.
- `config.py` is a strict Pydantic v2 schema (`extra="forbid"`). An unknown YAML key or `--set` path is an error, so a new option must be added to the schema. With `experiment.stage=test`, `data.cohort_path` and a registered `protocol_id` are required, and ad hoc filters are rejected.

Invariants that hold across files:

- **Test-leakage separation.** Solvers see only `PublicProblem` (statement plus public tests). Hidden suites (`prepared/<ds>/judge/suites/*.json`) are loaded only after `selected.py` has been saved, and only by `HiddenJudge`. Keep it that way.
- **Prepared data format.** `prepared/<ds>/public/problems.jsonl` plus one hidden-suite JSON per problem ID. Adding a dataset that already uses this schema only needs path changes. A new raw schema needs one adapter in `adapters/datasets/`, not solver changes.
- **Run artifacts (schema 2).** `manifest.json` fingerprints the effective config, cohort, data/source/prompt hashes and git revision. Each problem writes `problems/<id>/{candidates,evaluations,search,requests,feedback,usage,judge_results,completed}.json` and `selected.py`. A failure writes `error.json` and gets retried on resume. Resume works per completed problem, not mid-search, and only when the manifest matches. Large `problems/` trace dirs are partly gitignored, while `summary.json` files are tracked.
- **Budget accounting.** `total_model_calls` counts logical requests (expansion, code, rethink, critic, block analysis). Transport retries are reported separately, and unknown token usage is recorded as null, not 0.

## Other directories

- `data/cohorts/apps_benchmark_300.json` is the frozen APPS-300 cohort (seed 2027, 100 per difficulty level), used by every v3.1 APPS run; `data/cohorts/apps_pilot_20.json` is the pilot set outside it.
- `Agentic_AI.md`, `RAP_extracted.md`, `Rethink_extracted.md` and the PDFs are reference papers and notes. They are large, so don't load them unless needed.
