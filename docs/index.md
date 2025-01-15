# Welcome to Pepperpy Poetry Plugin

A Poetry plugin for shared configuration management across multiple projects in the pepperpy ecosystem.

## Overview

The Pepperpy Poetry Plugin is designed to simplify configuration management across multiple Python projects. It allows you to maintain a single source of truth for common configuration settings, ensuring consistency across your entire project ecosystem.

## Key Features

- **Shared Configuration Management**: Automatically merge shared configurations from `pepperpy.toml` into your project's `pyproject.toml`
- **Template System**: Rich template system with inheritance and variable substitution
- **Environment Variables**: Advanced environment variable management with validation
- **Caching**: Smart caching system for better performance
- **CLI Commands**: Intuitive commands for managing configurations and templates

## Quick Example

1. List available templates:
```bash
poetry pepperpy list-templates
```

2. Initialize a new project with a template:
```bash
poetry pepperpy init full
```

3. Or create a `pepperpy.toml` file manually:
```toml
# Use a predefined template
template = "full"

[tool.poetry]
name = "my-python-package"
description = "My Python Package"

[tool.pepperpy.env]
GH_TOKEN = { required = true, secret = true, description = "GitHub token for releases" }
POETRY_PYPI_TOKEN_PYPI = { required = true, secret = true, description = "PyPI token for publishing" }
```

## Available Templates

The plugin comes with several predefined templates:

### Base Template
Basic Python project setup with essential development tools.

### Full Template
Complete Python project setup with:
- Modern Python development tools (Ruff, Black, MyPy)
- Testing setup (Pytest with coverage)
- Documentation (Sphinx)
- CI/CD with semantic release
- Pre-commit hooks
- Automated version management

### FastAPI Template
Complete FastAPI web application setup with:
- FastAPI with Uvicorn
- Pydantic for data validation
- Authentication packages
- API testing tools

### CLI Template
Command-line application setup with:
- Typer for CLI interface
- Rich for beautiful terminal output
- Click testing utilities

### Data Science Template
Data science project setup with:
- NumPy and Pandas
- Scikit-learn
- Matplotlib and Seaborn
- Jupyter notebooks

### Django Template
Django web application setup with:
- Django with common extensions
- Environment management
- Authentication and forms
- Development tools

## Getting Started

Check out our [Quick Start Guide](getting-started/quick-start.md) to begin using the plugin in your projects.
