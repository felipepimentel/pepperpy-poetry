# Welcome to Pepperpy Poetry Plugin

A Poetry plugin for shared configuration management across multiple projects in the pepperpy ecosystem.

## Overview

The Pepperpy Poetry Plugin is designed to simplify configuration management across multiple Python projects. It allows you to maintain a single source of truth for common configuration settings, ensuring consistency across your entire project ecosystem.

## Key Features

- **Shared Configuration Management**: Automatically merge shared configurations from `shared-config.toml` into your project's `pyproject.toml`
- **Flexible Configuration**: Support for any TOML configuration sections
- **User-Friendly**: Clear console feedback during configuration merging
- **Error Handling**: Graceful handling of missing configuration files and errors

## Quick Example

1. Create a `shared-config.toml` in your project root:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
extend-exclude = [
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".git",
    "__pycache__"
]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
```

2. The plugin will automatically merge these configurations into your project's `pyproject.toml` when Poetry runs.

## Getting Started

Check out our [Quick Start Guide](getting-started/quick-start.md) to begin using the plugin in your projects.
