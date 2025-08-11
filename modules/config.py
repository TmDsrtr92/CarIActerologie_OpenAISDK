"""
Configuration Management for CarIActerology
Handles API keys, model settings, and application configuration from multiple sources.
"""

import os
import logging
from typing import Dict, Optional, Any
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class ConfigManager:
    """
    Centralized configuration manager for CarIActerology.
    
    Handles configuration from multiple sources in order of priority:
    1. Streamlit secrets (when running in Streamlit)
    2. Environment variables
    3. .env file (when available)
    4. Default values
    """
    
    def __init__(self, env_file: Optional[str] = None, validate: bool = True):
        """
        Initialize configuration manager.
        
        Args:
            env_file: Path to .env file (defaults to .env in project root)
            validate: Whether to validate required configuration on initialization
        """
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables from .env file if available
        if DOTENV_AVAILABLE:
            if env_file:
                load_dotenv(env_file)
            else:
                # Try to find .env in project root
                project_root = Path(__file__).parent.parent
                env_path = project_root / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
                    self.logger.info(f"Loaded environment from {env_path}")
        
        # Cache for configuration values
        self._config_cache = {}
        
        if validate:
            self._validate_required_config()
    
    def get_api_keys(self) -> Dict[str, Optional[str]]:
        """
        Get all API keys from configuration sources.
        
        Returns:
            Dictionary of API keys (None for missing keys)
        """
        keys = {
            "OPENAI_API_KEY": self._get_config("OPENAI_API_KEY", required=True),
            "MEM0_API_KEY": self._get_config("MEM0_API_KEY", required=False),
            "ANTHROPIC_API_KEY": self._get_config("ANTHROPIC_API_KEY", required=False),
            "GROQ_API_KEY": self._get_config("GROQ_API_KEY", required=False)
        }
        
        return keys
    
    def get_model_config(self) -> Dict[str, Any]:
        """
        Get LLM and embedding model configuration.
        
        Returns:
            Model configuration dictionary
        """
        return {
            "default_llm_model": self._get_config("DEFAULT_LLM_MODEL", default="gpt-4o-mini"),
            "default_embedding_model": self._get_config("DEFAULT_EMBEDDING_MODEL", default="text-embedding-3-small"),
            "fallback_llm_model": self._get_config("FALLBACK_LLM_MODEL", default="gpt-3.5-turbo"),
            "max_tokens": self._get_config("MAX_TOKENS", default=4000, cast_type=int),
            "temperature": self._get_config("TEMPERATURE", default=0.1, cast_type=float),
            "max_embedding_batch_size": self._get_config("MAX_EMBEDDING_BATCH_SIZE", default=100, cast_type=int)
        }
    
    def get_faiss_config(self) -> Dict[str, Any]:
        """
        Get FAISS database configuration.
        
        Returns:
            FAISS configuration dictionary
        """
        return {
            "index_path": self._get_config("FAISS_INDEX_PATH", default="data/characterology_faiss.index"),
            "metadata_path": self._get_config("FAISS_METADATA_PATH", default="data/characterology_metadata.pkl"),
            "index_type": self._get_config("FAISS_INDEX_TYPE", default="IndexFlatIP"),
        }
    
    def get_mem0_config(self) -> Dict[str, Any]:
        """
        Get Mem0 memory system configuration.
        
        Returns:
            Mem0 configuration dictionary
        """
        api_keys = self.get_api_keys()
        model_config = self.get_model_config()
        
        return {
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": model_config["default_embedding_model"],
                    "api_key": api_keys["OPENAI_API_KEY"]
                }
            },
            "vector_store": {
                "provider": "faiss",
                "config": {
                    "collection_name": self._get_config("MEM0_COLLECTION_NAME", default="characterology_memories"),
                    "path": self._get_config("MEM0_FAISS_PATH", default="data/mem0_faiss.index")
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": model_config["default_llm_model"],
                    "api_key": api_keys["OPENAI_API_KEY"],
                    "temperature": model_config["temperature"]
                }
            },
            "version": "v1.1"
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """
        Get general application configuration.
        
        Returns:
            Application configuration dictionary
        """
        return {
            "app_name": self._get_config("APP_NAME", default="CarIActerology"),
            "app_version": self._get_config("APP_VERSION", default="1.0.0"),
            "debug_mode": self._get_config("DEBUG_MODE", default=False, cast_type=bool),
            "development_mode": self._get_config("DEVELOPMENT_MODE", default=True, cast_type=bool),
            "log_level": self._get_config("LOG_LEVEL", default="INFO"),
            "session_timeout_minutes": self._get_config("SESSION_TIMEOUT_MINUTES", default=30, cast_type=int),
            "memory_cache_size": self._get_config("MEMORY_CACHE_SIZE", default=1000, cast_type=int)
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """
        Get security configuration.
        
        Returns:
            Security configuration dictionary
        """
        return {
            "session_secret": self._get_config("SESSION_SECRET_KEY", required=False),
            "encryption_key": self._get_config("ENCRYPTION_KEY", required=False)
        }
    
    def is_streamlit_environment(self) -> bool:
        """Check if running in Streamlit environment."""
        return STREAMLIT_AVAILABLE and hasattr(st, 'secrets')
    
    def is_development_mode(self) -> bool:
        """Check if in development mode."""
        return self._get_config("DEVELOPMENT_MODE", default=True, cast_type=bool)
    
    def _get_config(
        self, 
        key: str, 
        default: Any = None, 
        required: bool = False,
        cast_type: type = str
    ) -> Any:
        """
        Get configuration value from multiple sources.
        
        Args:
            key: Configuration key
            default: Default value if not found
            required: Whether this configuration is required
            cast_type: Type to cast the value to
            
        Returns:
            Configuration value
            
        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Check cache first
        if key in self._config_cache:
            return self._config_cache[key]
        
        value = None
        
        # Priority 1: Streamlit secrets
        if STREAMLIT_AVAILABLE:
            try:
                # Try api_keys section first
                if key.endswith("_API_KEY"):
                    value = st.secrets.get("api_keys", {}).get(key)
                
                # Try other sections
                if value is None:
                    sections_to_check = ["model_config", "app_config", "faiss_config", "mem0_config", "security"]
                    for section in sections_to_check:
                        section_data = st.secrets.get(section, {})
                        if key.lower() in section_data:
                            value = section_data[key.lower()]
                            break
                        elif key in section_data:
                            value = section_data[key]
                            break
                
                # Try direct access
                if value is None and key in st.secrets:
                    value = st.secrets[key]
                    
            except (KeyError, FileNotFoundError, AttributeError):
                pass
        
        # Priority 2: Environment variables
        if value is None:
            value = os.getenv(key)
        
        # Priority 3: Default value
        if value is None:
            if required:
                raise ConfigurationError(f"Required configuration '{key}' not found")
            value = default
        
        # Type casting
        if value is not None and cast_type != str:
            try:
                if cast_type == bool:
                    # Handle boolean conversion properly
                    if isinstance(value, str):
                        value = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        value = bool(value)
                else:
                    value = cast_type(value)
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Failed to cast {key} to {cast_type}: {e}")
                if required:
                    raise ConfigurationError(f"Invalid type for required configuration '{key}'")
                value = default
        
        # Cache the result
        self._config_cache[key] = value
        return value
    
    def _validate_required_config(self):
        """Validate that all required configuration is present."""
        try:
            # Check required API keys
            openai_key = self._get_config("OPENAI_API_KEY", required=True)
            if not openai_key or openai_key.startswith("sk-dummy"):
                raise ConfigurationError(
                    "OPENAI_API_KEY is not configured or still contains dummy value. "
                    "Please set your actual OpenAI API key in .env or Streamlit secrets."
                )
            
            self.logger.info("Configuration validation passed")
            
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(f"Configuration validation failed: {e}")
    
    def get_all_config(self) -> Dict[str, Any]:
        """
        Get all configuration as a single dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return {
            "api_keys": self.get_api_keys(),
            "model_config": self.get_model_config(),
            "faiss_config": self.get_faiss_config(),
            "mem0_config": self.get_mem0_config(),
            "app_config": self.get_app_config(),
            "security_config": self.get_security_config()
        }
    
    def print_config_summary(self, hide_secrets: bool = True):
        """
        Print configuration summary for debugging.
        
        Args:
            hide_secrets: Whether to hide sensitive values
        """
        config = self.get_all_config()
        
        print("=== CarIActerology Configuration Summary ===")
        print(f"Environment: {'Streamlit' if self.is_streamlit_environment() else 'Local'}")
        print(f"Development Mode: {config['app_config']['development_mode']}")
        print(f"LLM Model: {config['model_config']['default_llm_model']}")
        print(f"Embedding Model: {config['model_config']['default_embedding_model']}")
        
        # API Keys status
        print("\nAPI Keys Status:")
        for key, value in config["api_keys"].items():
            if value:
                if hide_secrets:
                    masked_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
                    print(f"  {key}: {masked_value} ✓")
                else:
                    print(f"  {key}: {value} ✓")
            else:
                print(f"  {key}: Not set ✗")
        
        print("\nConfiguration Sources:")
        print(f"  .env file: {'Available' if DOTENV_AVAILABLE else 'Not available'}")
        print(f"  Streamlit secrets: {'Available' if self.is_streamlit_environment() else 'Not available'}")


# Global configuration instance (lazy initialization)
config = None

def get_config() -> ConfigManager:
    """Get global configuration instance (lazy initialization)."""
    global config
    if config is None:
        config = ConfigManager(validate=False)  # Don't validate on import
    return config


# Convenience functions for common configuration access
def get_openai_api_key() -> str:
    """Get OpenAI API key."""
    key = get_config().get_api_keys()["OPENAI_API_KEY"]
    if not key:
        raise ConfigurationError("OpenAI API key not configured")
    return key


def get_model_settings() -> Dict[str, Any]:
    """Get model configuration."""
    return get_config().get_model_config()


def get_faiss_settings() -> Dict[str, Any]:
    """Get FAISS configuration."""
    return get_config().get_faiss_config()


def get_mem0_settings() -> Dict[str, Any]:
    """Get Mem0 configuration."""
    return get_config().get_mem0_config()


def is_development() -> bool:
    """Check if in development mode."""
    return get_config().is_development_mode()


# Example usage and testing
if __name__ == "__main__":
    try:
        # Test configuration loading
        config_instance = ConfigManager(validate=False)
        config_instance.print_config_summary()
        
        print("\n=== Testing Configuration Access ===")
        
        # Test API key access
        try:
            openai_key = get_openai_api_key()
            print(f"OpenAI API Key: {openai_key[:10]}... ✓")
        except ConfigurationError as e:
            print(f"OpenAI API Key: {e} ✗")
        
        # Test model settings
        model_settings = get_model_settings()
        print(f"Default LLM: {model_settings['default_llm_model']} ✓")
        print(f"Embedding Model: {model_settings['default_embedding_model']} ✓")
        
        # Test FAISS settings
        faiss_settings = get_faiss_settings()
        print(f"FAISS Index Path: {faiss_settings['index_path']} ✓")
        
        print("\nConfiguration test completed successfully!")
        
    except Exception as e:
        print(f"Configuration test failed: {e}")
        print("\nPlease ensure you have:")
        print("1. Replaced dummy API keys in .env or .streamlit/secrets.toml")
        print("2. Installed required packages: pip install python-dotenv")
        print("3. Set at least OPENAI_API_KEY with your actual key")