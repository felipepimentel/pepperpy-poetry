from pathlib import Path
from typing import Any, Dict, Optional, List
import os
import json
from datetime import datetime

import toml
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from cleo.io.io import IO
from poetry.utils.env import EnvManager
from poetry.console.application import Application

from .config import PepperpyConfig
from .commands import ListTemplatesCommand, InitCommand, ValidateCommand


class SharedConfigPlugin(Plugin):
    CONFIG_FILE = "pepperpy.toml"
    PLUGIN_NAME = "pepperpy-poetry"
    CACHE_DIR = ".pepperpy"
    CACHE_FILE = "config_cache.json"

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._cache_path: Optional[Path] = None
        self._last_config_path: Optional[Path] = None
        self._config: Optional[PepperpyConfig] = None

    def activate(self, poetry: Poetry, io: IO) -> None:
        """
        Activate the plugin and merge shared configurations.
        
        Args:
            poetry: The Poetry instance
            io: The IO instance for console output
        """
        try:
            # Register commands
            application = poetry.create_application()
            application.add(ListTemplatesCommand())
            application.add(InitCommand())
            application.add(ValidateCommand())

            self._setup_cache_dir(io)
            self._process_configuration(poetry, io)
        except Exception as e:
            io.error_line(f"[{self.PLUGIN_NAME}] Fatal error: {str(e)}")
            raise

    def _setup_cache_dir(self, io: IO) -> None:
        """
        Set up the cache directory for the plugin.
        
        Args:
            io: The IO instance for console output
        """
        cache_dir = Path.home() / self.CACHE_DIR
        cache_dir.mkdir(exist_ok=True)
        self._cache_path = cache_dir / self.CACHE_FILE
        
        if self._cache_path.exists():
            try:
                with open(self._cache_path) as f:
                    self._cache = json.load(f)
                io.write_line(f"[{self.PLUGIN_NAME}] Loaded configuration cache")
            except Exception as e:
                io.write_line(f"[{self.PLUGIN_NAME}] Failed to load cache: {str(e)}")
                self._cache = {}

    def _save_cache(self, config_path: Path, config: Dict[str, Any]) -> None:
        """
        Save the configuration to cache.
        
        Args:
            config_path: Path to the configuration file
            config: Configuration dictionary
        """
        if self._cache_path and self._config and self._config.cache.enabled:
            cache_entry = {
                "path": str(config_path),
                "last_modified": datetime.fromtimestamp(config_path.stat().st_mtime).isoformat(),
                "config": config
            }
            
            # Maintain cache size limit
            cache_items = list(self._cache.items())
            if len(cache_items) >= self._config.cache.max_size:
                # Remove oldest entries
                cache_items.sort(key=lambda x: datetime.fromisoformat(x[1]["last_modified"]))
                self._cache = dict(cache_items[-self._config.cache.max_size:])
            
            self._cache[str(config_path)] = cache_entry
            
            with open(self._cache_path, "w") as f:
                json.dump(self._cache, f, indent=2)

    def _is_cache_valid(self, config_path: Path) -> bool:
        """
        Check if the cache for a given config path is valid.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            bool: True if cache is valid, False otherwise
        """
        if not self._config or not self._config.cache.enabled:
            return False
            
        if str(config_path) not in self._cache:
            return False
            
        cache_entry = self._cache[str(config_path)]
        cache_mtime = datetime.fromisoformat(cache_entry["last_modified"])
        file_mtime = datetime.fromtimestamp(config_path.stat().st_mtime)
        
        # Check TTL
        cache_age = datetime.now() - cache_mtime
        if cache_age.total_seconds() > self._config.cache.ttl:
            return False
        
        return cache_mtime >= file_mtime

    def _process_configuration(self, poetry: Poetry, io: IO) -> None:
        """
        Process the pepperpy configuration file.
        
        Args:
            poetry: The Poetry instance
            io: The IO instance for console output
        """
        config_path = self._find_config_file()
        
        if config_path:
            io.write_line(f"[{self.PLUGIN_NAME}] Found configuration at: {config_path}")
            
            try:
                # Load and parse configuration
                raw_config = self._load_config(config_path)
                self._config = PepperpyConfig(raw_config)
                
                # Validate configuration
                validation_errors = self._config.validate()
                if validation_errors:
                    for error in validation_errors:
                        io.error_line(f"[{self.PLUGIN_NAME}] Validation error: {error}")
                    raise ValueError("Configuration validation failed")
                
                # Check cache first
                if self._is_cache_valid(config_path):
                    io.write_line(f"[{self.PLUGIN_NAME}] Using cached configuration")
                    shared_config = self._cache[str(config_path)]["config"]
                else:
                    # Get merged configuration with template if specified
                    template_name = raw_config.get("tool", {}).get("pepperpy", {}).get("template")
                    shared_config = self._config.get_merged_config(template_name)
                    self._save_cache(config_path, shared_config)
                    io.write_line(f"[{self.PLUGIN_NAME}] Configuration cached")
                
                # Merge configurations
                self._merge_configurations(poetry, shared_config)
                io.write_line(f"[{self.PLUGIN_NAME}] Configuration merged successfully")
                
                # Store last used config path
                self._last_config_path = config_path
                
            except toml.TomlDecodeError as e:
                io.error_line(f"[{self.PLUGIN_NAME}] Error parsing {self.CONFIG_FILE}: {str(e)}")
                raise
            except ValueError as e:
                io.error_line(f"[{self.PLUGIN_NAME}] Invalid configuration: {str(e)}")
                raise
        else:
            io.write_line(f"[{self.PLUGIN_NAME}] No {self.CONFIG_FILE} found. Skipping.")

    def _find_config_file(self) -> Optional[Path]:
        """
        Find the pepperpy configuration file by walking up the directory tree.
        
        Returns:
            Optional[Path]: Path to the configuration file if found, None otherwise
        """
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            config_path = current_dir / self.CONFIG_FILE
            if config_path.exists():
                return config_path
            current_dir = current_dir.parent
        return None

    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """
        Load and parse the configuration file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dict[str, Any]: Parsed configuration
            
        Raises:
            toml.TomlDecodeError: If the file cannot be parsed
        """
        return toml.load(config_path)

    def _merge_configurations(self, poetry: Poetry, shared_config: Dict[str, Any]) -> None:
        """
        Merge shared configurations into the project's pyproject.toml
        
        Args:
            poetry: The Poetry instance
            shared_config: The shared configuration dictionary
        """
        # Skip pepperpy-specific sections
        skip_sections = {"tool.pepperpy"}
        
        for section, values in shared_config.items():
            if any(section.startswith(skip) for skip in skip_sections):
                continue
                
            if isinstance(values, dict):
                poetry.pyproject.data.setdefault(section, {}).update(values)
            else:
                poetry.pyproject.data[section] = values 