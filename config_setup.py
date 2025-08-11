"""
Configuration Setup Helper for CarIActerology
Quick setup script to validate and test configuration.
"""

import os
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

try:
    from config import ConfigManager, ConfigurationError
    print("✅ Configuration module imported successfully")
except ImportError as e:
    print(f"❌ Error importing configuration: {e}")
    print("Please ensure all modules are in the correct location.")
    print("Try running from the project root directory.")
    sys.exit(1)


def check_environment_setup():
    """Check if environment is properly set up."""
    print("🔍 CarIActerology Configuration Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    print(f"📄 .env file: {'✅ Found' if env_file.exists() else '❌ Not found'}")
    
    # Check if Streamlit secrets exist
    secrets_file = Path(".streamlit/secrets.toml")
    print(f"📄 Streamlit secrets: {'✅ Found' if secrets_file.exists() else '❌ Not found'}")
    
    # Check for dummy values
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            has_dummy = "dummy" in content.lower()
            print(f"🔑 API keys in .env: {'⚠️  Contains dummy values' if has_dummy else '✅ Looks configured'}")
    
    print()


def test_configuration():
    """Test configuration loading and validation."""
    print("🧪 Testing Configuration Loading")
    print("-" * 30)
    
    try:
        # Initialize configuration manager
        config = ConfigManager(validate=False)  # Don't validate initially to show details
        
        # Print configuration summary
        config.print_config_summary(hide_secrets=True)
        
        print("\n🔍 Detailed Configuration Test")
        print("-" * 30)
        
        # Test API keys
        api_keys = config.get_api_keys()
        for key, value in api_keys.items():
            if value:
                is_dummy = "dummy" in value.lower()
                status = "⚠️  Dummy value" if is_dummy else "✅ Configured"
                print(f"{key}: {status}")
            else:
                print(f"{key}: ❌ Not set")
        
        # Test required configuration
        print("\n🔧 Validating Required Configuration")
        print("-" * 30)
        
        try:
            ConfigManager(validate=True)  # This will validate required config
            print("✅ All required configuration is valid!")
            return True
        except ConfigurationError as e:
            print(f"❌ Configuration error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def provide_setup_instructions():
    """Provide setup instructions for missing configuration."""
    print("\n📋 Setup Instructions")
    print("=" * 50)
    
    print("1. 🔑 Set up your API keys:")
    print("   Replace the dummy values in .env with your actual keys:")
    print("   - Get OpenAI API key from: https://platform.openai.com/api-keys")
    print("   - Replace 'sk-dummy-openai-api-key-replace-with-your-actual-key-here'")
    print("   - With your actual OpenAI API key")
    
    print("\n2. 📦 Install required packages:")
    print("   pip install python-dotenv openai faiss-cpu mem0ai")
    
    print("\n3. 🧪 Test your configuration:")
    print("   python config_setup.py")
    
    print("\n4. 🚀 For Streamlit Cloud deployment:")
    print("   - Copy API keys from .env to .streamlit/secrets.toml")
    print("   - Or set them in Streamlit Cloud dashboard")


def main():
    """Main setup function."""
    print("🎯 CarIActerology Configuration Setup")
    print("=" * 50)
    
    # Check environment setup
    check_environment_setup()
    
    # Test configuration
    config_valid = test_configuration()
    
    if not config_valid:
        provide_setup_instructions()
        print("\n❌ Configuration setup incomplete.")
        print("Please follow the instructions above and run this script again.")
        return False
    else:
        print("\n✅ Configuration setup complete!")
        print("You can now run the CarIActerology application.")
        return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)