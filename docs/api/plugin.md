# Plugin API

## Overview

The Pepperpy Poetry Plugin provides a set of commands and APIs for managing shared configurations across Poetry projects.

## Commands

### List Templates

List all available templates and their details:

```bash
poetry pepperpy list-templates [--config=<path>]
```

Options:
- `--config`: Path to pepperpy.toml file (optional)

Example output:
```
Available templates:

base
  Description: Base template for Python projects
  Variables:
    PYTHON_VERSION = 3.9

fastapi
  Description: Template for FastAPI projects
  Extends: base
  Variables:
    PYTHON_VERSION = 3.9
    FASTAPI_VERSION = 0.109.0
```

### Initialize Project

Initialize a new project with a template:

```bash
poetry pepperpy init [template] [--config=<path>] [--force]
```

Arguments:
- `template`: Template to use (optional, interactive selection if not provided)

Options:
- `--config`: Path to pepperpy.toml file (optional)
- `--force`: Overwrite existing files

Example:
```bash
# Interactive template selection
poetry pepperpy init

# Use specific template
poetry pepperpy init fastapi

# Force overwrite existing files
poetry pepperpy init django --force
```

### Validate Configuration

Validate your pepperpy configuration:

```bash
poetry pepperpy validate [--config=<path>]
```

Options:
- `--config`: Path to pepperpy.toml file (optional)

Example output:
```
Configuration is valid.
```

Or with errors:
```
Configuration validation failed:
  - Invalid template 'unknown' referenced in extends
  - Required environment variable 'GITHUB_TOKEN' not set
```

## Plugin Class

### SharedConfigPlugin

The main plugin class that handles configuration management and command registration.

```python
class SharedConfigPlugin(Plugin):
    """Poetry plugin for shared configuration management."""
    
    CONFIG_FILE = "pepperpy.toml"
    PLUGIN_NAME = "pepperpy-poetry"
    CACHE_DIR = ".pepperpy"
    CACHE_FILE = "config_cache.json"
```

#### Methods

##### activate

```python
def activate(self, poetry: Poetry, io: IO) -> None:
    """
    Activate the plugin and merge shared configurations.
    
    Args:
        poetry: The Poetry instance
        io: The IO instance for console output
    """
```

This method:
1. Registers plugin commands
2. Sets up configuration cache
3. Processes and merges configurations

##### _process_configuration

```python
def _process_configuration(self, poetry: Poetry, io: IO) -> None:
    """
    Process the pepperpy configuration file.
    
    Args:
        poetry: The Poetry instance
        io: The IO instance for console output
    """
```

This method:
1. Finds the configuration file
2. Loads and validates configuration
3. Applies caching if enabled
4. Merges configurations into pyproject.toml

## Command Classes

### ListTemplatesCommand

```python
class ListTemplatesCommand(Command):
    """List available templates in the Pepperpy configuration."""
    
    name = "pepperpy list-templates"
```

### InitCommand

```python
class InitCommand(Command):
    """Initialize a new project with a template."""
    
    name = "pepperpy init"
```

### ValidateCommand

```python
class ValidateCommand(Command):
    """Validate the Pepperpy configuration."""
    
    name = "pepperpy validate"
```

## Usage Example

```python
from pepperpy_poetry.plugin import SharedConfigPlugin
from poetry.poetry import Poetry
from cleo.io.io import IO

# Create plugin instance
plugin = SharedConfigPlugin()

# Activate plugin
plugin.activate(poetry, io)

# Commands are now available through Poetry CLI
```
