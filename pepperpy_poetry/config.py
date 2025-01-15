from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import os
import re
from datetime import datetime, timedelta

@dataclass
class EnvVarConfig:
    """Configuration for an environment variable."""
    name: str
    required: bool = False
    default: Optional[str] = None
    description: Optional[str] = None
    secret: bool = False

@dataclass
class CacheConfig:
    """Configuration for caching."""
    enabled: bool = True
    ttl: int = 3600  # seconds
    max_size: int = 100  # number of entries

@dataclass
class TemplateConfig:
    """Configuration for templates."""
    name: str
    description: Optional[str] = None
    variables: Dict[str, str] = None
    extends: Optional[str] = None

class PepperpyConfig:
    """Main configuration class for Pepperpy."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        self.raw_config = config_dict
        self.env_vars: Dict[str, EnvVarConfig] = {}
        self.cache: CacheConfig = CacheConfig()
        self.templates: Dict[str, TemplateConfig] = {}
        self._parse_config()

    def _parse_config(self) -> None:
        """Parse the raw configuration into structured objects."""
        if "tool" in self.raw_config and "pepperpy" in self.raw_config["tool"]:
            pepperpy_config = self.raw_config["tool"]["pepperpy"]
            
            # Parse environment variables
            if "env" in pepperpy_config:
                for name, config in pepperpy_config["env"].items():
                    if isinstance(config, dict):
                        self.env_vars[name] = EnvVarConfig(
                            name=name,
                            required=config.get("required", False),
                            default=config.get("default"),
                            description=config.get("description"),
                            secret=config.get("secret", False)
                        )
            
            # Parse cache configuration
            if "cache" in pepperpy_config:
                cache_config = pepperpy_config["cache"]
                self.cache = CacheConfig(
                    enabled=cache_config.get("enabled", True),
                    ttl=cache_config.get("ttl", 3600),
                    max_size=cache_config.get("max_size", 100)
                )
            
            # Parse templates
            if "templates" in pepperpy_config:
                for name, config in pepperpy_config["templates"].items():
                    if isinstance(config, dict):
                        self.templates[name] = TemplateConfig(
                            name=name,
                            description=config.get("description"),
                            variables=config.get("variables", {}),
                            extends=config.get("extends")
                        )

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template configuration with all inherited values resolved.
        
        Args:
            name: Name of the template
            
        Returns:
            Optional[Dict[str, Any]]: Resolved template configuration or None if not found
        """
        if name not in self.templates:
            return None
            
        template = self.templates[name]
        config = {}
        
        # Handle template inheritance
        if template.extends:
            parent_config = self.get_template(template.extends)
            if parent_config:
                config.update(parent_config)
        
        # Apply template variables
        if template.variables:
            config.update(self._resolve_variables(template.variables))
        
        return config

    def _resolve_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve variables in configuration values.
        
        Args:
            config: Configuration dictionary with variables
            
        Returns:
            Dict[str, Any]: Configuration with resolved variables
        """
        resolved = {}
        var_pattern = re.compile(r"\$\{([^}]+)\}")
        
        def resolve_value(value: str) -> str:
            if not isinstance(value, str):
                return value
                
            matches = var_pattern.finditer(value)
            result = value
            
            for match in matches:
                var_name = match.group(1)
                var_value = os.environ.get(var_name)
                if var_value is None:
                    for env_var in self.env_vars.values():
                        if env_var.name == var_name and env_var.default is not None:
                            var_value = env_var.default
                            break
                
                if var_value is not None:
                    result = result.replace(f"${{{var_name}}}", var_value)
            
            return result
        
        for key, value in config.items():
            if isinstance(value, dict):
                resolved[key] = self._resolve_variables(value)
            elif isinstance(value, list):
                resolved[key] = [resolve_value(v) for v in value]
            else:
                resolved[key] = resolve_value(value)
        
        return resolved

    def get_merged_config(self, template_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the final configuration with template and variables resolved.
        
        Args:
            template_name: Optional template to apply
            
        Returns:
            Dict[str, Any]: Final resolved configuration
        """
        config = {}
        
        # Start with raw config
        for section, values in self.raw_config.items():
            if section != "tool" or "pepperpy" not in values:
                config[section] = values
        
        # Apply template if specified
        if template_name:
            template_config = self.get_template(template_name)
            if template_config:
                for section, values in template_config.items():
                    if isinstance(values, dict):
                        config.setdefault(section, {}).update(values)
                    else:
                        config[section] = values
        
        # Resolve variables
        return self._resolve_variables(config)

    def validate(self) -> List[str]:
        """
        Validate the configuration.
        
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        # Validate environment variables
        for env_var in self.env_vars.values():
            if env_var.required:
                value = os.environ.get(env_var.name)
                if value is None and env_var.default is None:
                    errors.append(f"Required environment variable {env_var.name} is not set")
        
        # Validate templates
        template_names = set(self.templates.keys())
        for template in self.templates.values():
            if template.extends and template.extends not in template_names:
                errors.append(f"Template {template.name} extends non-existent template {template.extends}")
        
        # Validate cache configuration
        if self.cache.ttl <= 0:
            errors.append("Cache TTL must be positive")
        if self.cache.max_size <= 0:
            errors.append("Cache max size must be positive")
        
        return errors 