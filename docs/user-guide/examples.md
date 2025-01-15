# Usage Examples

This guide provides practical examples of using the Pepperpy Poetry Plugin.

## Template Examples

### FastAPI Project

Create a new FastAPI project with authentication and API documentation:

```bash
# Initialize project
poetry pepperpy init fastapi

# Install dependencies
poetry install

# Run development server
poetry run uvicorn app.main:app --reload
```

Example `pepperpy.toml`:
```toml
template = "fastapi"

[tool.poetry]
name = "my-fastapi-app"
version = "0.1.0"
description = "My FastAPI Application"
authors = ["Felipe Pimentel <fpimentel88@gmail.com>"]

[tool.pepperpy.env]
JWT_SECRET = { required = true, secret = true, description = "Secret key for JWT tokens" }
DATABASE_URL = { required = true, description = "Database connection string" }
```

### CLI Application

Create a command-line tool with rich terminal output:

```bash
# Initialize project
poetry pepperpy init cli

# Install dependencies
poetry install

# Run CLI
poetry run python -m my_cli
```

Example `pepperpy.toml`:
```toml
template = "cli"

[tool.poetry]
name = "my-cli-tool"
version = "0.1.0"
description = "My CLI Tool"
authors = ["Felipe Pimentel <fpimentel88@gmail.com>"]

[tool.pepperpy.env]
CONFIG_PATH = { default = "~/.my-cli/config.json", description = "Configuration file path" }
LOG_LEVEL = { default = "INFO", description = "Logging level" }
```

### Data Science Project

Set up a data science environment with Jupyter notebooks:

```bash
# Initialize project
poetry pepperpy init data-science

# Install dependencies
poetry install

# Start Jupyter
poetry run jupyter notebook
```

Example `pepperpy.toml`:
```toml
template = "data-science"

[tool.poetry]
name = "my-data-project"
version = "0.1.0"
description = "My Data Science Project"
authors = ["Felipe Pimentel <fpimentel88@gmail.com>"]

[tool.pepperpy.env]
DATA_PATH = { required = true, description = "Path to data directory" }
MODEL_PATH = { default = "models", description = "Path to save trained models" }
```

### Django Web Application

Create a Django project with authentication and forms:

```bash
# Initialize project
poetry pepperpy init django

# Install dependencies
poetry install

# Run migrations
poetry run python manage.py migrate

# Start development server
poetry run python manage.py runserver
```

Example `pepperpy.toml`:
```toml
template = "django"

[tool.poetry]
name = "my-django-app"
version = "0.1.0"
description = "My Django Application"
authors = ["Felipe Pimentel <fpimentel88@gmail.com>"]

[tool.pepperpy.env]
DJANGO_SECRET_KEY = { required = true, secret = true, description = "Django secret key" }
DATABASE_URL = { required = true, description = "Database connection string" }
ALLOWED_HOSTS = { default = "localhost,127.0.0.1", description = "Allowed hosts" }
```

## Command Examples

### List Templates with Details

```bash
poetry pepperpy list-templates
```

### Initialize with Interactive Selection

```bash
poetry pepperpy init
```

### Initialize with Specific Template

```bash
poetry pepperpy init fastapi --force
```

### Validate Configuration

```bash
poetry pepperpy validate
```

### Using Custom Configuration Path

```bash
poetry pepperpy init --config=/path/to/pepperpy.toml
```

## Template Inheritance Example

Create a custom template that extends the base template:

```toml
[tool.pepperpy.templates.my-template]
description = "My custom template"
extends = "base"
variables = { 
    PYTHON_VERSION = "3.9",
    CUSTOM_VAR = "value"
}

[tool.pepperpy.templates.my-template.tool.poetry.dependencies]
requests = "^2.31.0"
pyyaml = "^6.0.1"

[tool.pepperpy.templates.my-template.tool.poetry.group.dev.dependencies]
pytest-mock = "^3.12.0"
```

## Environment Variables Example

Configure environment variables with validation:

```toml
[tool.pepperpy.env]
# Required secret
API_KEY = { 
    required = true, 
    secret = true, 
    description = "API key for external service" 
}

# Optional with default
CACHE_TTL = { 
    default = "3600", 
    description = "Cache time-to-live in seconds" 
}

# Dynamic value
PROJECT_NAME = { 
    default = "${POETRY_PROJECT}", 
    description = "Project name from Poetry" 
}

# Required with validation
LOG_LEVEL = { 
    required = true, 
    default = "INFO",
    description = "Logging level (DEBUG, INFO, WARNING, ERROR)" 
}
```

## CI/CD with GitHub Actions

When using the `full` template, you get a complete CI/CD setup with GitHub Actions. Here's what's included:

### Test and Lint Workflow

```yaml
name: Test and Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
      - name: Install dependencies
        run: poetry install
      - name: Run tests
        run: poetry run pytest
      - name: Run linting
        run: |
          poetry run ruff check .
          poetry run ruff format --check .
          poetry run mypy .

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
      - name: Install dependencies
        run: poetry install
      - name: Run security checks
        run: poetry run bandit -r src/
```

### Release Workflow

```yaml
name: Release

on:
  push:
    branches: [ main ]

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      id-token: write
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Python Semantic Release
        uses: python-semantic-release/python-semantic-release@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Pre-commit Hooks

The `full` template includes pre-commit hooks for code quality. Here's the configuration:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-all

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check
      - id: poetry-lock
```

To set up pre-commit hooks:

```bash
poetry run pre-commit install
```

## Release Process

The `full` template uses Python Semantic Release for automated versioning and publishing:

1. Write conventional commits:
```bash
# Features
git commit -m "feat: add new feature"

# Bug fixes
git commit -m "fix: resolve issue"

# Breaking changes
git commit -m "feat!: redesign API"
```

2. Push to main branch:
```bash
git push origin main
```

3. The release workflow will:
   - Determine the next version based on commits
   - Update version in pyproject.toml
   - Create a new GitHub release
   - Build and publish to PyPI

## Environment Variables

The `full` template includes robust environment variable validation:

```toml
[tool.pepperpy.env]
# Required for releases
GH_TOKEN = { 
    required = true, 
    secret = true, 
    description = "GitHub token for releases",
    pattern = "^gh[ps]_[A-Za-z0-9_]{36}$"
}

# PyPI token for publishing
POETRY_PYPI_TOKEN_PYPI = { 
    required = true, 
    secret = true, 
    description = "PyPI token for publishing",
    pattern = "^pypi-[A-Za-z0-9_-]{100,}$"
}

# Optional configuration
LOG_LEVEL = { 
    default = "INFO", 
    description = "Logging level",
    choices = ["DEBUG", "INFO", "WARNING", "ERROR"]
}
```

## Cache Configuration

Advanced caching options:

```toml
[tool.pepperpy.cache]
enabled = true
ttl = 3600  # Cache time-to-live in seconds
max_size = 100  # Maximum number of cached configurations
cleanup_interval = 86400  # Cleanup old cache entries daily
```

## Commands

### Update Dependencies

```bash
# Update all dependencies
poetry pepperpy update-deps

# Update specific dependencies
poetry pepperpy update-deps pytest ruff

# Check for updates without applying
poetry pepperpy update-deps --check
```

### Validate CI/CD

```bash
# Validate GitHub Actions workflows
poetry pepperpy validate-ci

# Validate specific workflow
poetry pepperpy validate-ci .github/workflows/test.yml
```

### Generate Configurations

```bash
# Generate all config files
poetry pepperpy generate-config

# Generate specific config
poetry pepperpy generate-config pre-commit
poetry pepperpy generate-config github-actions
```

## Update Python Version

Update Python version across all configuration files:

```bash
# Update to specific version
poetry pepperpy update-python 3.12.0

# Update using version from .python-version
poetry pepperpy update-python
```

This will update:
- `.python-version` file
- Python version in `pyproject.toml`
- Template configurations

## Common Project Files

The base template includes common configuration files:

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: poetry run pytest
        language: system
        pass_filenames: false
        always_run: true
        
      - id: ruff-check
        name: ruff check
        entry: poetry run ruff check --fix .
        language: system
        pass_filenames: false
        always_run: true
        
      - id: ruff-format
        name: ruff format
        entry: poetry run ruff format .
        language: system
        pass_filenames: false
        always_run: true
```

### Python Version

```text
# .python-version
3.12.0
```

### Dagger Configuration

```json
# dagger.json
{
    "name": "${PROJECT_NAME}",
    "sdk": "python"
}
```

### VSCode Settings

```json
# .vscode/settings.json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll": true,
        "source.organizeImports": true
    },
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

### Pytest Configuration

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
addopts = --cov=${PROJECT_NAME} --cov-report=term-missing --cov-report=xml
filterwarnings =
    ignore::pytest.PytestCollectionWarning
    ignore::pytest.PytestReturnNotNoneWarning
    ignore::pytest.PytestUnraisableExceptionWarning
    ignore::RuntimeWarning
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

You can generate these files using:

```bash
poetry pepperpy generate-config
```

Or generate specific files:

```bash
poetry pepperpy generate-config pre-commit
poetry pepperpy generate-config python-version
poetry pepperpy generate-config dagger
```

## Documentation

### Build and Deploy

Build and deploy documentation to GitHub Pages:

```bash
# Deploy to GitHub Pages
poetry pepperpy docs

# Serve locally
poetry pepperpy docs --serve

# Serve on specific port
poetry pepperpy docs --serve --port 8080
```

The documentation is built using MkDocs with the Material theme and includes:
- API Reference with automatic docstring parsing
- Code syntax highlighting
- Dark/light mode support
- Full-text search
- Mobile-friendly responsive design

### Configuration

The base template includes MkDocs configuration in `mkdocs.yml`:

```yaml
site_name: Your Project Name
site_description: Your project description
site_author: Your Name
repo_url: https://github.com/username/repo
repo_name: username/repo

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true

nav:
  - Home: index.md
  - API Reference: api.md
```
