import json
import logging
from typing import List, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    @abstractmethod
    def generate_thoughts(self, problem_desc: str, previous_thoughts: List[str], k: int = 3) -> List[str]:
        """Sinh k chiến lược / bước tư duy tiếp theo."""
        pass

    @abstractmethod
    def generate_code(self, problem_desc: str, thoughts: List[str]) -> str:
        """Sinh mã nguồn Python hoàn chỉnh dựa trên các bước tư duy đã tích lũy."""
        pass

    @abstractmethod
    def rethink_thought(self, problem_desc: str, previous_thoughts: List[str], erroneous_thought: str, code: str, feedback: str) -> str:
        """Thực hiện cơ chế Rethink: tinh chỉnh nút tư duy lỗi dựa trên phản hồi kiểm thử."""
        pass

    @abstractmethod
    def self_evaluate(self, problem_desc: str, code: str) -> float:
        """LLM tự chấm điểm độ tin cậy của mã nguồn khi đã vượt qua các public test cases."""
        pass


class OpenAILLMClient(BaseLLMClient):
    """Client giao tiếp với Ollama hoặc vLLM Server thông qua OpenAI-compatible HTTP API."""
    def __init__(self, api_base: str = "http://localhost:11434/v1", api_key: str = "ollama", model_name: str = "qwen2.5-coder:7b"):
        import requests
        self.requests = requests
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key
        self.model_name = model_name

    def _chat_completion(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        url = f"{self.api_base}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        resp = self.requests.post(url, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"] or ""

    def generate_thoughts(self, problem_desc: str, previous_thoughts: List[str], k: int = 3) -> List[str]:
        thoughts_context = "\n".join([f"- Thought {i+1}: {t}" for i, t in enumerate(previous_thoughts)]) if previous_thoughts else "None"
        prompt = f"""Problem Description:
{problem_desc}

Current reasoning steps:
{thoughts_context}

Please propose {k} distinct reasoning strategies or thought steps to solve this problem.
Output each thought on a single line starting with '- '."""

        content = self._chat_completion(prompt, temperature=0.7, max_tokens=512)
        lines = []
        for line in content.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith(("- ", "* ", "• ")):
                lines.append(s[2:].strip())
            elif s[0].isdigit() and len(s) > 2 and s[1] in (".", ")", ":"):
                lines.append(s[2:].strip())
            elif s[:2].isdigit() and len(s) > 3 and s[2] in (".", ")", ":"):
                lines.append(s[3:].strip())
        return lines[:k] if lines else [content.strip()]

    def generate_code(self, problem_desc: str, thoughts: List[str]) -> str:
        thoughts_context = "\n".join([f"Step {i+1}: {t}" for i, t in enumerate(thoughts)])
        prompt = f"""Problem Description:
{problem_desc}

Algorithm and Reasoning Steps:
{thoughts_context}

Write a complete, self-contained Python 3 solution that reads from standard input (sys.stdin) and prints to standard output (sys.stdout).
Return ONLY the python code inside a ```python ``` codeblock."""

        content = self._chat_completion(prompt, temperature=0.2, max_tokens=1024)
        if "```python" in content:
            code = content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            code = content.split("```")[1].split("```")[0].strip()
        else:
            code = content.strip()
        return code

    def rethink_thought(self, problem_desc: str, previous_thoughts: List[str], erroneous_thought: str, code: str, feedback: str) -> str:
        prompt = f"""Problem Description:
{problem_desc}

Previous Reasoning:
{chr(10).join(previous_thoughts[:-1]) if len(previous_thoughts) > 1 else 'None'}

Erroneous Thought:
{erroneous_thought}

Generated Code that failed:
```python
{code}
```

Test Feedback:
{feedback}

Based on the execution error, refine and fix the erroneous thought. Explain what was wrong and provide the corrected strategy in 1-2 clear sentences."""

        return self._chat_completion(prompt, temperature=0.3, max_tokens=256).strip()

    def self_evaluate(self, problem_desc: str, code: str) -> float:
        import re
        prompt = f"""Problem:
{problem_desc}

Code:
```python
{code}
```

All public test cases passed. Rate the correctness and robustness for unseen edge cases from 0.0 to 1.0.
Output only a single number between 0.0 and 1.0."""

        text = self._chat_completion(prompt, temperature=0.0, max_tokens=32).strip()
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        if match:
            try:
                val = float(match.group(1))
                if 1.0 < val <= 10.0:
                    val = val / 10.0
                elif 10.0 < val <= 100.0:
                    val = val / 100.0
                return max(0.0, min(1.0, val))
            except ValueError:
                pass
        return 0.8


class MockLLMClient(BaseLLMClient):
    """
    Mock LLM Client giả lập hành vi của mô hình ngôn ngữ cho mục đích kiểm thử MVP nội bộ
    mà không cần tốn chi phí Cloud GPU.
    """
    def __init__(self):
        self.rethink_called = False

    def generate_thoughts(self, problem_desc: str, previous_thoughts: List[str], k: int = 3) -> List[str]:
        if not previous_thoughts:
            return [
                "Strategy A: Check if the number is simply even by evaluating w % 2 == 0.",
                "Strategy B: Divide the number into halves and check parity.",
                "Strategy C: Iterate all pairs of positive integers (a, b) such that a + b = w."
            ][:k]
        return [f"Refining further: Ensure input constraints are satisfied for {previous_thoughts[-1]}"]

    def generate_code(self, problem_desc: str, thoughts: List[str]) -> str:
        last_thought = thoughts[-1] if thoughts else ""
        # Nếu chưa rethink và chứa tư duy ngây thơ (chỉ check w % 2 == 0 không check w > 2)
        if "Strategy A" in last_thought or ("w % 2 == 0" in last_thought and not self.rethink_called):
            return "w = int(input())\nif w % 2 == 0:\n    print('YES')\nelse:\n    print('NO')\n"
        # Sau khi rethink hoặc với tư duy đã sửa
        return "w = int(input())\nif w % 2 == 0 and w > 2:\n    print('YES')\nelse:\n    print('NO')\n"

    def rethink_thought(self, problem_desc: str, previous_thoughts: List[str], erroneous_thought: str, code: str, feedback: str) -> str:
        self.rethink_called = True
        return "Rethink Strategy: While w must be even, each part must be a POSITIVE even integer (>= 2). Thus 2 cannot be divided into two positive evens. We must check w % 2 == 0 AND w > 2."

    def self_evaluate(self, problem_desc: str, code: str) -> float:
        return 0.95
