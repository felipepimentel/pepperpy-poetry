# Configuration API

## Overview

The Pepperpy Poetry Plugin uses a robust configuration system that supports:
- Environment variable management
- Configuration caching
- Template inheritance
- Variable substitution

## Classes

### PepperpyConfig

Main configuration class that handles all configuration aspects of the plugin.

```python
class PepperpyConfig:
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize configuration from a dictionary.
        
        Args:
            config_dict: Raw configuration dictionary from pepperpy.toml
        """
```

#### Methods

##### get_template

```python
def get_template(self, name: str) -> Optional[Dict[str, Any]]:
    """
    Get a template configuration with all inherited values resolved.
    
    Args:
        name: Name of the template
        
    Returns:
        Optional[Dict[str, Any]]: Resolved template configuration or None if not found
    """
```

##### get_merged_config

```python
def get_merged_config(self, template_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the final configuration with template and variables resolved.
    
    Args:
        template_name: Optional template to apply
        
    Returns:
        Dict[str, Any]: Final resolved configuration
    """
```

##### validate

```python
def validate(self) -> List[str]:
    """
    Validate the configuration.
    
    Returns:
        List[str]: List of validation errors
    """
```

### EnvVarConfig

Configuration for environment variables.

```python
@dataclass
class EnvVarConfig:
    name: str
    required: bool = False
    default: Optional[str] = None
    description: Optional[str] = None
    secret: bool = False
```

#### Fields

- `name`: Name of the environment variable
- `required`: Whether the variable is required
- `default`: Default value if not set
- `description`: Description of the variable's purpose
- `secret`: Whether the variable contains sensitive data

### CacheConfig

Configuration for the caching system.

```python
@dataclass
class CacheConfig:
    enabled: bool = True
    ttl: int = 3600  # seconds
    max_size: int = 100  # number of entries
```

#### Fields

- `enabled`: Whether caching is enabled
- `ttl`: Time-to-live in seconds for cached entries
- `max_size`: Maximum number of entries in the cache

### TemplateConfig

Configuration for templates.

```python
@dataclass
class TemplateConfig:
    name: str
    description: Optional[str] = None
    variables: Dict[str, str] = None
    extends: Optional[str] = None
```

#### Fields

- `name`: Name of the template
- `description`: Description of the template's purpose
- `variables`: Dictionary of template variables
- `extends`: Name of the template to extend

## Usage Examples

### Environment Variables

```toml
[tool.pepperpy.env]
GITHUB_TOKEN = { required = true, secret = true, description = "GitHub Personal Access Token" }
AWS_REGION = { default = "us-east-1", description = "AWS Region for deployment" }
```

### Templates

```toml
[tool.pepperpy.templates.base]
description = "Base template for Python projects"
extends = "minimal"
variables = { PYTHON_VERSION = "3.9" }

[tool.pepperpy.templates.base.tool.poetry]
python = "^${PYTHON_VERSION}"
```

### Cache Configuration

```toml
[tool.pepperpy.cache]
enabled = true
ttl = 3600  # Cache time-to-live in seconds
max_size = 100  # Maximum number of cached configurations
```

## Variable Substitution

The plugin supports variable substitution in configuration values using the `${VARIABLE}` syntax:

- Environment variables: `${ENV_VAR}`
- Template variables: `${TEMPLATE_VAR}`
- Poetry variables: `${POETRY_PROJECT}`, `${POETRY_VERSION}`

Example:
```toml
[tool.poetry]
description = "Project ${POETRY_PROJECT} version ${POETRY_VERSION}"
python = "^${PYTHON_VERSION}"
``` 