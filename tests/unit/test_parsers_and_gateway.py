"""
Unit tests U14 to U17 verifying parsers, gateway URL normalization, and strict configuration.
"""

import pytest
from rethink_mcts.adapters.llm.parsing import (
    parse_thoughts_json,
    extract_python_code,
    parse_critic_score
)
from rethink_mcts.adapters.llm.http_gateway import normalize_base_url
from rethink_mcts.config import AppConfig
from rethink_mcts.domain.errors import InvalidModelOutputError, ConfigurationError


def test_u14_proposals_json_not_tricked_by_explanation_numbers():
    """
    U14: Model output có số trong explanation trước score -> Đọc JSON field đúng, không lấy số đầu bằng regex.
    """
    raw_output = """Here are 2 strategies for solving the task (analyzing 100 test cases first):
```json
{
  "thoughts": [
    {
      "text": "Strategy 1: check if number mod 2 is 0",
      "reasonableness": 0.7
    },
    {
      "text": "Strategy 2: divide by 2 and check parity of 4 factors",
      "reasonableness": 0.3
    }
  ]
}
```
"""
    proposals = parse_thoughts_json(raw_output)
    assert len(proposals) == 2
    # The scores must be 0.7 and 0.3, NOT 2, 100, 1, or 4!
    assert proposals[0][1] == 0.7
    assert proposals[1][1] == 0.3


def test_u15_multiple_conflicting_code_blocks_raises():
    """
    U15: Code nhiều fence/truncated -> Invalid/truncated có typed error, không sửa tùy tiện.
    """
    conflicting_code = """Here is option 1:
```python
print("Option 1")
```

And here is option 2:
```python
print("Option 2")
```
"""
    with pytest.raises(InvalidModelOutputError) as exc:
        extract_python_code(conflicting_code)
    assert "conflicting code blocks" in str(exc.value).lower()


def test_u16_url_normalization_handles_various_formats():
    """
    U16: URL base/full endpoint/prefix/trailing slash -> Route đúng, không duplicate path.
    """
    # 1. Base URL with trailing slash
    assert normalize_base_url("http://localhost:11434/v1/") == "http://localhost:11434/v1"

    # 2. Full endpoint with chat/completions
    assert normalize_base_url("http://localhost:11434/v1/chat/completions") == "http://localhost:11434/v1"

    # 3. Custom reverse proxy prefix with trailing slash
    assert normalize_base_url("http://proxy.internal:8000/proxy/llm/v1/") == "http://proxy.internal:8000/proxy/llm/v1"

    # 4. Custom reverse proxy with full path
    assert normalize_base_url("http://proxy.internal:8000/proxy/llm/v1/chat/completions/") == "http://proxy.internal:8000/proxy/llm/v1"


def test_u17_unsupported_config_field_fail_fast():
    """
    U17: Unsupported config field/range -> Fail-fast, không bỏ qua config.
    """
    # 1. Extra forbidden field
    bad_dict = {
        "schema_version": 1,
        "unexpected_extra_field": "illegal_value"
    }
    with pytest.raises(ConfigurationError):
        # We simulate YAML load of invalid field
        import yaml
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yaml") as f:
            yaml.dump(bad_dict, f)
            f.flush()
            AppConfig.from_yaml_file(f.name)

    # 2. Invalid range (critic min >= max)
    invalid_range_dict = {
        "reward": {
            "critic_score_min": 1.0,
            "critic_score_max": 0.0  # min > max is illegal!
        }
    }
    with pytest.raises(ConfigurationError):
        import yaml
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yaml") as f:
            yaml.dump(invalid_range_dict, f)
            f.flush()
            AppConfig.from_yaml_file(f.name)


def test_u19_block_analysis_parsing_supports_paper_list_and_dict():
    from rethink_mcts.adapters.llm.semantic import SemanticPromptedLLM
    from rethink_mcts.domain.feedback import ExecutionFacts, TraceResult, BlockVerdict
    from rethink_mcts.ports.models import GenerationResponse

    class MockGateway:
        def __init__(self, response_text):
            self.response_text = response_text
        def complete(self, req):
            return GenerationResponse(self.response_text, "stop", prompt_tokens=10, completion_tokens=10)

    # 1. Paper Table 14 list format
    paper_json = """[
        {"block": "bb_1", "correct": "True", "explanation": "Initializes loop"},
        {"block": "bb_2", "correct": "False", "explanation": "Off by one error"}
    ]"""
    model = SemanticPromptedLLM(MockGateway(paper_json), "prompts/compact_v1")
    analysis = model.analyze("problem", "code", ExecutionFacts("WA", "", "", ""), TraceResult("success"))
    assert len(analysis.assessments) == 2
    assert analysis.assessments[0].block_id == "bb_1"
    assert analysis.assessments[0].verdict == BlockVerdict.CORRECT
    assert analysis.assessments[1].block_id == "bb_2"
    assert analysis.assessments[1].verdict == BlockVerdict.INCORRECT

    # 2. Boolean values and fenced markdown
    bool_json = """```json
    [
        {"block_id": "bb_1", "correct": false, "explanation": "Failed condition"}
    ]
    ```"""
    model.gateway = MockGateway(bool_json)
    analysis2 = model.analyze("problem", "code", ExecutionFacts("WA", "", "", ""), TraceResult("success"))
    assert len(analysis2.assessments) == 1
    assert analysis2.assessments[0].verdict == BlockVerdict.INCORRECT

    # 3. Dict format with assessments
    dict_json = """{
        "summary": "Boundary error",
        "assessments": [
            {"block_id": "bb_1", "verdict": "correct", "explanation": "Valid"}
        ]
    }"""
    model.gateway = MockGateway(dict_json)
    analysis3 = model.analyze("problem", "code", ExecutionFacts("WA", "", "", ""), TraceResult("success"))
    assert len(analysis3.assessments) == 1
    assert analysis3.summary_explanation == "Boundary error"
