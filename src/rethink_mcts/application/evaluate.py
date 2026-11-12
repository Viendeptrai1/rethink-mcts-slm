"""
Candidate evaluation coordinator implementing conditional self-evaluation and dual reward.
"""

import uuid
import hashlib
import json
from dataclasses import asdict
from rethink_mcts.application.model_calls import invoke_model
from typing import Optional
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord, SelfEvalStatus
from rethink_mcts.domain.problem import PublicProblem
from rethink_mcts.domain.budget import BudgetManager
from rethink_mcts.ports.execution import PublicExecutor
from rethink_mcts.ports.models import CodeCritic
from rethink_mcts.policies.reward import PaperDualRewardPolicy


class CandidateEvaluator:
    def __init__(
        self,
        executor: PublicExecutor,
        critic: Optional[CodeCritic],
        reward_policy: PaperDualRewardPolicy
    ):
        self.executor = executor
        self.critic = critic
        self.reward_policy = reward_policy

    def evaluate_public(
        self,
        candidate: ProgramCandidate,
        problem: PublicProblem,
        budget: Optional[BudgetManager] = None
    ) -> EvaluationRecord:
        eval_id = f"eval_{uuid.uuid4().hex[:10]}"

        if budget is not None:
            budget.reserve_sandbox_runs(len(problem.public_tests))
        # 1. Execute public test suite
        exec_summary = self.executor.evaluate(
            candidate=candidate,
            tests=problem.public_tests,
            spec=problem.execution_spec,
            limits=problem.limits
        )
        if budget is not None:
            budget.record_evaluation_event()
            budget.usage.valid_candidates += 1
            budget.program_hashes.add(candidate.code_hash)
            budget.usage.unique_programs = len(budget.program_hashes)

        # 2. Check conditional LLM critic call
        v_test = exec_summary.pass_rate
        v_llm: Optional[float] = None
        self_eval_status = SelfEvalStatus.SKIPPED_NOT_ALL_PASSED

        if self.reward_policy.should_call_critic(exec_summary) and self.critic is not None:
            try:
                if budget is not None:
                    raw_score = invoke_model(budget, self.critic, "assess", "critic",
                                             statement=problem.statement, candidate_code=candidate.code,
                                             active_thoughts=tuple(candidate.thought_path_snapshot or ()))
                else:
                    raw_score = self.critic.assess(statement=problem.statement, candidate_code=candidate.code,
                                                   active_thoughts=tuple(candidate.thought_path_snapshot or ()))
                v_llm = max(self.reward_policy.critic_min, min(self.reward_policy.critic_max, float(raw_score)))
                self_eval_status = SelfEvalStatus.EVALUATED
            except Exception:
                self_eval_status = SelfEvalStatus.UNAVAILABLE_FALLBACK
                v_llm = 0.0

        # 3. Compute final reward
        reward = self.reward_policy.compute_reward(exec_summary, v_llm=v_llm)

        return EvaluationRecord(
            evaluation_id=eval_id,
            candidate_id=candidate.candidate_id,
            suite_visibility="public",
            suite_hash=hashlib.sha256(json.dumps([asdict(c) for c in problem.public_tests], sort_keys=True).encode()).hexdigest(),
            execution_summary=exec_summary,
            v_test=v_test,
            self_eval_raw=v_llm,
            self_eval_status=self_eval_status,
            reward=reward,
            reward_policy_id="dual",
            backup_committed=False
        )
