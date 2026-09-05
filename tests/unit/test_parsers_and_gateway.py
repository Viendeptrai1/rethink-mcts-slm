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
