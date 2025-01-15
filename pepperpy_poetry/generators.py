"""Configuration file generators."""
from pathlib import Path
from typing import Optional
import json

import yaml
from cleo.io.io import IO


def generate_pre_commit(io: Optional[IO] = None) -> int:
    """Generate pre-commit configuration."""
    config = {
        "repos": [
            {
                "repo": "https://github.com/astral-sh/ruff-pre-commit",
                "rev": "v0.3.0",
                "hooks": [
                    {
                        "id": "ruff",
                        "args": ["--fix"]
                    },
                    {
                        "id": "ruff-format"
                    }
                ]
            },
            {
                "repo": "https://github.com/pre-commit/mirrors-mypy",
                "rev": "v1.9.0",
                "hooks": [
                    {
                        "id": "mypy",
                        "additional_dependencies": ["types-all"]
                    }
                ]
            },
            {
                "repo": "https://github.com/python-poetry/poetry",
                "rev": "1.7.0",
                "hooks": [
                    {"id": "poetry-check"},
                    {"id": "poetry-lock"}
                ]
            }
        ]
    }

    try:
        config_path = Path(".pre-commit-config.yaml")
        if config_path.exists():
            if io:
                io.write_error("<error>.pre-commit-config.yaml already exists</error>")
            return 1

        with open(config_path, "w") as f:
            yaml.safe_dump(config, f, sort_keys=False)

        if io:
            io.write_line("<info>Generated .pre-commit-config.yaml</info>")
        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error generating pre-commit config: {str(e)}</error>")
        return 1


def generate_github_actions(io: Optional[IO] = None) -> int:
    """Generate GitHub Actions workflows."""
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Test and Lint workflow
    test_workflow = {
        "name": "Test and Lint",
        "on": {
            "push": {"branches": ["main"]},
            "pull_request": {"branches": ["main"]}
        },
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v4"},
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v5",
                        "with": {"python-version": "3.12"}
                    },
                    {
                        "name": "Install Poetry",
                        "run": "curl -sSL https://install.python-poetry.org | python3 -"
                    },
                    {
                        "name": "Install dependencies",
                        "run": "poetry install"
                    },
                    {
                        "name": "Run tests",
                        "run": "poetry run pytest"
                    },
                    {
                        "name": "Run linting",
                        "run": "\n".join([
                            "poetry run ruff check .",
                            "poetry run ruff format --check .",
                            "poetry run mypy ."
                        ])
                    }
                ]
            },
            "security": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v4"},
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v5",
                        "with": {"python-version": "3.12"}
                    },
                    {
                        "name": "Install Poetry",
                        "run": "curl -sSL https://install.python-poetry.org | python3 -"
                    },
                    {
                        "name": "Install dependencies",
                        "run": "poetry install"
                    },
                    {
                        "name": "Run security checks",
                        "run": "poetry run bandit -r src/"
                    }
                ]
            }
        }
    }

    # Release workflow
    release_workflow = {
        "name": "Release",
        "on": {
            "push": {"branches": ["main"]}
        },
        "jobs": {
            "release": {
                "runs-on": "ubuntu-latest",
                "concurrency": "release",
                "permissions": {
                    "id-token": "write",
                    "contents": "write"
                },
                "steps": [
                    {
                        "uses": "actions/checkout@v4",
                        "with": {"fetch-depth": 0}
                    },
                    {
                        "name": "Python Semantic Release",
                        "uses": "python-semantic-release/python-semantic-release@master",
                        "with": {
                            "github_token": "${{ secrets.GITHUB_TOKEN }}"
                        }
                    }
                ]
            }
        }
    }

    try:
        # Write test workflow
        test_path = workflows_dir / "test.yml"
        if not test_path.exists():
            with open(test_path, "w") as f:
                yaml.safe_dump(test_workflow, f, sort_keys=False)
            if io:
                io.write_line("<info>Generated .github/workflows/test.yml</info>")

        # Write release workflow
        release_path = workflows_dir / "release.yml"
        if not release_path.exists():
            with open(release_path, "w") as f:
                yaml.safe_dump(release_workflow, f, sort_keys=False)
            if io:
                io.write_line("<info>Generated .github/workflows/release.yml</info>")

        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error generating GitHub Actions workflows: {str(e)}</error>")
        return 1


def validate_github_actions(workflow_path: Optional[str] = None, io: Optional[IO] = None) -> int:
    """Validate GitHub Actions workflows."""
    try:
        workflows_dir = Path(".github/workflows")
        if not workflows_dir.exists():
            if io:
                io.write_error("<error>No GitHub Actions workflows found</error>")
            return 1

        if workflow_path:
            workflow_files = [Path(workflow_path)]
            if not workflow_files[0].exists():
                if io:
                    io.write_error(f"<error>Workflow file {workflow_path} not found</error>")
                return 1
        else:
            workflow_files = list(workflows_dir.glob("*.yml"))

        for workflow_file in workflow_files:
            try:
                with open(workflow_file) as f:
                    yaml.safe_load(f)
                if io:
                    io.write_line(f"<info>✓ {workflow_file} is valid</info>")
            except yaml.YAMLError as e:
                if io:
                    io.write_error(f"<error>✗ {workflow_file} is invalid: {str(e)}</error>")
                return 1

        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error validating workflows: {str(e)}</error>")
        return 1


def generate_python_version(io: Optional[IO] = None) -> int:
    """Generate .python-version file."""
    try:
        version_path = Path(".python-version")
        if version_path.exists():
            if io:
                io.write_error("<error>.python-version already exists</error>")
            return 1

        with open(version_path, "w") as f:
            f.write("3.12.0\n")

        if io:
            io.write_line("<info>Generated .python-version</info>")
        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error generating .python-version: {str(e)}</error>")
        return 1


def generate_dagger_config(project_name: str, io: Optional[IO] = None) -> int:
    """Generate dagger.json file."""
    try:
        dagger_path = Path("dagger.json")
        if dagger_path.exists():
            if io:
                io.write_error("<error>dagger.json already exists</error>")
            return 1

        config = {
            "name": project_name,
            "sdk": "python"
        }

        with open(dagger_path, "w") as f:
            json.dump(config, f)

        if io:
            io.write_line("<info>Generated dagger.json</info>")
        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error generating dagger.json: {str(e)}</error>")
        return 1 