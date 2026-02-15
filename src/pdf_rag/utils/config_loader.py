"""
Configuration Loader Module

This module handles loading and managing YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import logging
import os

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage configuration from YAML files."""
    
    def __init__(self, config_dir: str = "configs"):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self.configs = {}
        
        logger.info(f"ConfigLoader initialized with directory: {self.config_dir}")
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load a configuration file.
        
        Args:
            config_file: Name of the configuration file (e.g., 'model_config.yaml')
            
        Returns:
            Dictionary containing configuration
        """
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Replace environment variables
            config = self._replace_env_vars(config)
            
            self.configs[config_file] = config
            logger.info(f"Loaded configuration from {config_file}")
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration from {config_file}: {str(e)}")
            raise
    
    def _replace_env_vars(self, config: Any) -> Any:
        """
        Recursively replace environment variable placeholders in config.
        
        Args:
            config: Configuration value (can be dict, list, str, etc.)
            
        Returns:
            Configuration with environment variables replaced
        """
        if isinstance(config, dict):
            return {k: self._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._replace_env_vars(item) for item in config]
        elif isinstance(config, str):
            # Replace ${VAR_NAME} with environment variable value
            if config.startswith("${") and config.endswith("}"):
                var_name = config[2:-1]
                return os.getenv(var_name, config)
            return config
        else:
            return config
    
    def get_config(self, config_file: str) -> Dict[str, Any]:
        """
        Get a loaded configuration or load it if not already loaded.
        
        Args:
            config_file: Name of the configuration file
            
        Returns:
            Configuration dictionary
        """
        if config_file not in self.configs:
            return self.load_config(config_file)
        return self.configs[config_file]
    
    def reload_config(self, config_file: str) -> Dict[str, Any]:
        """
        Reload a configuration file.
        
        Args:
            config_file: Name of the configuration file
            
        Returns:
            Reloaded configuration dictionary
        """
        return self.load_config(config_file)
