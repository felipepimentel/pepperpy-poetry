# Plugin API

## Overview

The Pepperpy Poetry Plugin provides a set of commands and APIs for managing shared configurations across Poetry projects.

## Commands

### Update Dependencies

Update project dependencies with shared configurations:

```bash
poetry pepperpy update-deps [--check]
```

Options:
- `--check`: Check for updates without applying them

### Validate CI Configuration

Validate CI/CD workflow files:

```bash
poetry pepperpy validate-ci [workflow]
```

Arguments:
- `workflow`: Path to workflow file (optional)

### Generate Configuration

Generate configuration files:

```bash
poetry pepperpy generate-config [type]
```

Arguments:
- `type`: Type of configuration to generate (pre-commit, github-actions, python-version, dagger)

### Update Python Version

Update Python version across configuration files:

```bash
poetry pepperpy update-python [version]
```

Arguments:
- `version`: Python version to set (optional, reads from .python-version if not provided)

### Build Documentation

Build and deploy documentation:

```bash
poetry pepperpy docs [--serve] [--port=<port>]
```

Options:
- `--serve`: Serve documentation locally
- `--port`: Port to serve documentation on (default: 8000)

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

##### commands

```python
def commands(self) -> List[Command]:
    """Return the list of commands provided by this plugin."""
```

This method returns the list of commands that the plugin provides:
- UpdateDependenciesCommand
- ValidateCICommand
- GenerateConfigCommand
- UpdatePythonVersionCommand
- BuildDocsCommand

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
1. Sets up configuration cache
2. Processes and merges configurations

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

### UpdateDependenciesCommand

```python
class UpdateDependenciesCommand(Command):
    """Update project dependencies with shared configurations."""
    
    name = "pepperpy update-deps"
```

### ValidateCICommand

```python
class ValidateCICommand(Command):
    """Validate CI/CD workflow files."""
    
    name = "pepperpy validate-ci"
```

### GenerateConfigCommand

```python
class GenerateConfigCommand(Command):
    """Generate configuration files."""
    
    name = "pepperpy generate-config"
```

### UpdatePythonVersionCommand

```python
class UpdatePythonVersionCommand(Command):
    """Update Python version across configuration files."""
    
    name = "pepperpy update-python"
```

### BuildDocsCommand

```python
class BuildDocsCommand(Command):
    """Build and deploy documentation."""
    
    name = "pepperpy docs"
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
