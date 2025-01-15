# Quick Start Guide

This guide will help you get started with the Pepperpy Poetry Plugin.

## Installation

You can install the plugin using any of these methods:

### Using `pipx` (Recommended)

```bash
pipx inject poetry pepperpy-poetry
```

### Using Poetry's plugin manager

```bash
poetry self add pepperpy-poetry
```

### Using pip in Poetry's environment

```bash
$POETRY_HOME/bin/pip install pepperpy-poetry
```

## Basic Usage

### 1. List Available Templates

First, check what templates are available:

```bash
poetry pepperpy list-templates
```

This will show you all available templates with their descriptions and variables.

### 2. Initialize a New Project

You can initialize a new project using any of the available templates:

```bash
# Interactive template selection
poetry pepperpy init

# Or specify a template directly
poetry pepperpy init fastapi
```

This will create a new `pyproject.toml` with all the necessary configurations.

### 3. Manual Configuration

Alternatively, you can create a `pepperpy.toml` file manually:

```toml
# Use a predefined template
template = "fastapi"

[tool.poetry]
name = "my-fastapi-app"
version = "0.1.0"
description = "My FastAPI Application"
authors = ["Felipe Pimentel <fpimentel88@gmail.com>"]

[tool.pepperpy.env]
GITHUB_TOKEN = { required = true, secret = true }
AWS_REGION = { default = "us-east-1" }
```

### 4. Validate Configuration

You can validate your configuration at any time:

```bash
poetry pepperpy validate
```

## Available Templates

The plugin comes with several predefined templates for different types of projects:

### Base Template

Basic Python project setup:
```bash
poetry pepperpy init base
```

### FastAPI Template

Complete FastAPI web application setup:
```bash
poetry pepperpy init fastapi
```

Includes:
- FastAPI with Uvicorn
- Pydantic for data validation
- Authentication packages
- API testing tools

### CLI Template

Command-line application setup:
```bash
poetry pepperpy init cli
```

Includes:
- Typer for CLI interface
- Rich for beautiful terminal output
- Click testing utilities

### Data Science Template

Data science project setup:
```bash
poetry pepperpy init data-science
```

Includes:
- NumPy and Pandas
- Scikit-learn
- Matplotlib and Seaborn
- Jupyter notebooks

### Django Template

Django web application setup:
```bash
poetry pepperpy init django
```

Includes:
- Django with common extensions
- Environment management
- Authentication and forms
- Development tools

### Full Template

Complete Python project setup with modern tools:
```bash
poetry pepperpy init full
```

Includes:
- Modern Python development tools (Ruff, Black, MyPy)
- Testing setup (Pytest with coverage)
- Documentation (Sphinx)
- CI/CD with semantic release
- Pre-commit hooks
- Automated version management
- Coverage reporting
- Type checking configuration

Example usage:
```toml
template = "full"

[tool.poetry]
name = "my-python-package"
description = "My Python Package"

[tool.pepperpy.env]
GH_TOKEN = { required = true, secret = true, description = "GitHub token for releases" }
POETRY_PYPI_TOKEN_PYPI = { required = true, secret = true, description = "PyPI token for publishing" }
```

## Next Steps

- Learn more about [Configuration](../user-guide/configuration.md)
- Check out [Usage Examples](../user-guide/examples.md)
- Explore the [API Reference](../api/index.md)
