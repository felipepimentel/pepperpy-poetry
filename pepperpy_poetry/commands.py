"""Commands for the Pepperpy Poetry Plugin."""
from pathlib import Path
from typing import List, Optional

import click
from cleo.helpers import argument, option
from poetry.console.commands.command import Command
from poetry.core.pyproject.toml import PyProjectTOML
from poetry.plugins.application_plugin import ApplicationPlugin

from .config import PepperpyConfig
from .generators import (
    generate_github_actions,
    generate_pre_commit,
    generate_python_version,
    generate_dagger_config,
    validate_github_actions
)
from .dependency import update_dependencies


class UpdateDependenciesCommand(Command):
    """Update project dependencies."""

    name = "pepperpy update-deps"
    description = "Update project dependencies to their latest versions."

    arguments = [
        argument(
            "packages",
            "The packages to update.",
            optional=True,
            multiple=True
        )
    ]
    options = [
        option(
            "check",
            None,
            "Check for updates without applying them.",
            flag=True
        )
    ]

    def handle(self) -> int:
        """Handle the command."""
        packages = self.argument("packages")
        check_only = self.option("check")
        
        return update_dependencies(
            packages=packages,
            check_only=check_only,
            io=self.io
        )


class ValidateCICommand(Command):
    """Validate CI/CD configuration."""

    name = "pepperpy validate-ci"
    description = "Validate GitHub Actions workflows."

    arguments = [
        argument(
            "workflow",
            "The workflow file to validate.",
            optional=True
        )
    ]

    def handle(self) -> int:
        """Handle the command."""
        workflow = self.argument("workflow")
        return validate_github_actions(workflow, self.io)


class GenerateConfigCommand(Command):
    """Generate configuration files."""

    name = "pepperpy generate-config"
    description = "Generate configuration files (pre-commit, GitHub Actions, python-version, dagger)."

    arguments = [
        argument(
            "config_type",
            "The type of configuration to generate (pre-commit, github-actions, python-version, dagger).",
            optional=True
        )
    ]

    def handle(self) -> int:
        """Handle the command."""
        config_type = self.argument("config_type")
        
        if not config_type or config_type == "pre-commit":
            generate_pre_commit(self.io)
        
        if not config_type or config_type == "github-actions":
            generate_github_actions(self.io)
            
        if not config_type or config_type == "python-version":
            generate_python_version(self.io)
            
        if not config_type or config_type == "dagger":
            # Get project name from pyproject.toml
            pyproject = PyProjectTOML(Path("pyproject.toml"))
            project_name = pyproject.poetry_config.get("name", "")
            generate_dagger_config(project_name, self.io)
        
        return 0


class UpdatePythonVersionCommand(Command):
    """Update Python version."""

    name = "pepperpy update-python"
    description = "Update Python version across all configuration files."

    arguments = [
        argument(
            "version",
            "The Python version to use (e.g. 3.12.0).",
            optional=True
        )
    ]

    def handle(self) -> int:
        """Handle the command."""
        version = self.argument("version")
        if not version:
            # Try to get version from .python-version
            try:
                with open(".python-version") as f:
                    version = f.read().strip()
            except FileNotFoundError:
                self.line_error("<error>No version specified and .python-version not found</error>")
                return 1
        
        # Update .python-version
        try:
            with open(".python-version", "w") as f:
                f.write(f"{version}\n")
            self.line("<info>Updated .python-version</info>")
        except Exception as e:
            self.line_error(f"<error>Error updating .python-version: {str(e)}</error>")
            return 1
        
        # Update pyproject.toml Python version
        try:
            pyproject = PyProjectTOML(Path("pyproject.toml"))
            content = pyproject.read()
            major_minor = ".".join(version.split(".")[:2])
            content = content.replace(
                'PYTHON_VERSION = "3.12"',
                f'PYTHON_VERSION = "{major_minor}"'
            )
            pyproject.write(content)
            self.line("<info>Updated Python version in pyproject.toml</info>")
        except Exception as e:
            self.line_error(f"<error>Error updating pyproject.toml: {str(e)}</error>")
            return 1
        
        return 0


class PepperpyApplicationPlugin(ApplicationPlugin):
    """Pepperpy Poetry Plugin."""

    def activate(self, application):
        """Activate the plugin."""
        application.command_loader.register_factory(
            "pepperpy update-deps",
            lambda: UpdateDependenciesCommand()
        )
        application.command_loader.register_factory(
            "pepperpy validate-ci",
            lambda: ValidateCICommand()
        )
        application.command_loader.register_factory(
            "pepperpy generate-config",
            lambda: GenerateConfigCommand()
        )
        application.command_loader.register_factory(
            "pepperpy update-python",
            lambda: UpdatePythonVersionCommand()
        ) 