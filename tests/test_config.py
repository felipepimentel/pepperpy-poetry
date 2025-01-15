import os
from pathlib import Path
import pytest
from pepperpy_poetry.config import PepperpyConfig, EnvVarConfig, CacheConfig, TemplateConfig

@pytest.fixture
def sample_config():
    return {
        "tool": {
            "pepperpy": {
                "env": {
                    "TEST_VAR": {"required": True, "default": "test", "description": "Test variable"},
                    "OPTIONAL_VAR": {"required": False, "default": "optional"},
                },
                "cache": {
                    "enabled": True,
                    "ttl": 3600,
                    "max_size": 100,
                },
                "templates": {
                    "base": {
                        "description": "Base template",
                        "variables": {"VERSION": "1.0.0"},
                    },
                    "extended": {
                        "description": "Extended template",
                        "extends": "base",
                        "variables": {"AUTHOR": "Test Author"},
                    },
                },
            }
        }
    }

def test_env_var_config():
    config = EnvVarConfig(
        name="TEST_VAR",
        required=True,
        default="test",
        description="Test variable",
        secret=False
    )
    assert config.name == "TEST_VAR"
    assert config.required
    assert config.default == "test"
    assert config.description == "Test variable"
    assert not config.secret

def test_cache_config():
    config = CacheConfig(enabled=True, ttl=3600, max_size=100)
    assert config.enabled
    assert config.ttl == 3600
    assert config.max_size == 100

def test_template_config():
    config = TemplateConfig(
        name="test",
        description="Test template",
        variables={"VERSION": "1.0.0"},
        extends="base"
    )
    assert config.name == "test"
    assert config.description == "Test template"
    assert config.variables == {"VERSION": "1.0.0"}
    assert config.extends == "base"

def test_pepperpy_config_initialization(sample_config):
    config = PepperpyConfig(sample_config)
    assert len(config.env_vars) == 2
    assert config.cache.enabled
    assert len(config.templates) == 2

def test_template_inheritance(sample_config):
    config = PepperpyConfig(sample_config)
    template = config.get_template("extended")
    assert template is not None
    assert "VERSION" in template.get("variables", {})
    assert "AUTHOR" in template.get("variables", {})

def test_variable_resolution(sample_config):
    os.environ["TEST_ENV_VAR"] = "env_value"
    config = PepperpyConfig(sample_config)
    resolved = config._resolve_variables({
        "value": "${TEST_ENV_VAR}",
        "nested": {"another": "${TEST_VAR}"}
    })
    assert resolved["value"] == "env_value"
    assert resolved["nested"]["another"] == "test"

def test_validation(sample_config):
    config = PepperpyConfig(sample_config)
    errors = config.validate()
    assert not errors  # No errors expected

def test_validation_with_errors():
    invalid_config = {
        "tool": {
            "pepperpy": {
                "cache": {
                    "ttl": -1  # Invalid TTL
                },
                "templates": {
                    "invalid": {
                        "extends": "non_existent"  # Invalid template extension
                    }
                }
            }
        }
    }
    config = PepperpyConfig(invalid_config)
    errors = config.validate()
    assert len(errors) == 2  # Two validation errors expected

def test_merged_config(sample_config):
    config = PepperpyConfig(sample_config)
    merged = config.get_merged_config("extended")
    assert merged is not None
    assert "tool" in merged 