"""Poetry commands for the Pepperpy plugin."""
from pathlib import Path
from typing import List, Optional
from cleo.helpers import argument, option
from poetry.console.commands.command import Command
from poetry.poetry import Poetry
from .config import PepperpyConfig
import toml

class ListTemplatesCommand(Command):
    """
    List available templates in the Pepperpy configuration.

    pepperpy list-templates
        {--config= : Path to pepperpy.toml file}
    """

    name = "pepperpy list-templates"

    def handle(self) -> int:
        """Execute the command."""
        config_path = self.option("config")
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self._find_config_file()

        if not config_file:
            self.line("<error>No pepperpy.toml file found.</error>")
            return 1

        try:
            config_dict = toml.load(config_file)
            config = PepperpyConfig(config_dict)

            self.line("<info>Available templates:</info>")
            for name, template in config.templates.items():
                self.line(f"\n<comment>{name}</comment>")
                if template.description:
                    self.line(f"  Description: {template.description}")
                if template.extends:
                    self.line(f"  Extends: {template.extends}")
                if template.variables:
                    self.line("  Variables:")
                    for var_name, var_value in template.variables.items():
                        self.line(f"    {var_name} = {var_value}")

            return 0

        except Exception as e:
            self.line(f"<error>Error loading templates: {str(e)}</error>")
            return 1

    def _find_config_file(self) -> Optional[Path]:
        """Find the pepperpy configuration file."""
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            config_path = current_dir / "pepperpy.toml"
            if config_path.exists():
                return config_path
            current_dir = current_dir.parent
        return None

class InitCommand(Command):
    """
    Initialize a new project with a template.

    pepperpy init
        {template? : Template to use}
        {--config= : Path to pepperpy.toml file}
        {--force : Overwrite existing files}
    """

    name = "pepperpy init"

    def handle(self) -> int:
        """Execute the command."""
        template_name = self.argument("template")
        config_path = self.option("config")
        force = self.option("force")

        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self._find_config_file()

        if not config_file:
            self.line("<error>No pepperpy.toml file found.</error>")
            return 1

        try:
            config_dict = toml.load(config_file)
            config = PepperpyConfig(config_dict)

            if not template_name:
                # Interactive template selection
                choices = list(config.templates.keys())
                if not choices:
                    self.line("<error>No templates available.</error>")
                    return 1

                template_name = self.choice(
                    "Select a template to use",
                    choices,
                    default=choices[0]
                )

            if template_name not in config.templates:
                self.line(f"<error>Template '{template_name}' not found.</error>")
                return 1

            # Get merged configuration
            merged_config = config.get_merged_config(template_name)

            # Create pyproject.toml
            pyproject_path = Path.cwd() / "pyproject.toml"
            if pyproject_path.exists() and not force:
                self.line("<error>pyproject.toml already exists. Use --force to overwrite.</error>")
                return 1

            with open(pyproject_path, "w") as f:
                toml.dump(merged_config, f)

            self.line(f"<info>Project initialized with template '{template_name}'.</info>")
            return 0

        except Exception as e:
            self.line(f"<error>Error initializing project: {str(e)}</error>")
            return 1

    def _find_config_file(self) -> Optional[Path]:
        """Find the pepperpy configuration file."""
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            config_path = current_dir / "pepperpy.toml"
            if config_path.exists():
                return config_path
            current_dir = current_dir.parent
        return None

class ValidateCommand(Command):
    """
    Validate the Pepperpy configuration.

    pepperpy validate
        {--config= : Path to pepperpy.toml file}
    """

    name = "pepperpy validate"

    def handle(self) -> int:
        """Execute the command."""
        config_path = self.option("config")
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self._find_config_file()

        if not config_file:
            self.line("<error>No pepperpy.toml file found.</error>")
            return 1

        try:
            config_dict = toml.load(config_file)
            config = PepperpyConfig(config_dict)

            errors = config.validate()
            if errors:
                self.line("<error>Configuration validation failed:</error>")
                for error in errors:
                    self.line(f"  - {error}")
                return 1

            self.line("<info>Configuration is valid.</info>")
            return 0

        except Exception as e:
            self.line(f"<error>Error validating configuration: {str(e)}</error>")
            return 1

    def _find_config_file(self) -> Optional[Path]:
        """Find the pepperpy configuration file."""
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            config_path = current_dir / "pepperpy.toml"
            if config_path.exists():
                return config_path
            current_dir = current_dir.parent
        return None 