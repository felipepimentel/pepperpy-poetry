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
