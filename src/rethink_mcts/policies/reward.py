"""
Dual reward policy following Paper Eq. 3 and spec §6.4.
"""

from typing import Optional
from rethink_mcts.domain.candidate import ExecutionSummary


class PaperDualRewardPolicy:
    """
    Reward computation according to Paper Eq. 3:
    v_test = public_passed / public_total
    reward = v_test                      if v_test < 1
    reward = a * v_test + b * v_llm      if v_test == 1
    """
    def __init__(
        self,
        test_weight: float = 0.8,
        llm_weight: float = 0.2,
        critic_min: float = 0.0,
        critic_max: float = 1.0
    ):
        self.a = test_weight
        self.b = llm_weight
        self.critic_min = critic_min
        self.critic_max = critic_max

    def should_call_critic(self, execution_summary: ExecutionSummary) -> bool:
        """
        Only call critic if all public tests passed and total > 0 (U04).
        """
        return execution_summary.all_passed and execution_summary.total > 0

    def compute_reward(
        self,
        execution_summary: ExecutionSummary,
        v_llm: Optional[float] = None
    ) -> Optional[float]:
        """
        Computes final reward:
        - None if total == 0 (NO_TESTS) (U08).
        - v_test if v_test < 1.0 (critic not used) (U04).
        - a * v_test + b * v_llm if v_test == 1.0 (U05, U06, U07). Note: NEVER clamped!
        """
        if execution_summary.total == 0 or execution_summary.pass_rate is None:
            return None

        v_test = execution_summary.pass_rate
        if v_test < 1.0 or not execution_summary.all_passed:
            return v_test

        # All passed: combine with critic
        if v_llm is None:
            # If critic was not available or skipped, fall back to v_test
            return v_test

        # Do not clamp final reward (U07)
        return self.a * v_test + self.b * v_llm
