"""
Quick configuration test script
Tests that configuration can be imported and used without validation errors.
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

def test_config_import():
    """Test that config module can be imported."""
    try:
        print("🧪 Testing configuration module import...")
        from config import ConfigManager, ConfigurationError, get_config
        print("✅ Configuration module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config_creation():
    """Test creating configuration manager without validation."""
    try:
        print("🧪 Testing configuration manager creation...")
        from config import ConfigManager
        
        # Create without validation (should work even with dummy keys)
        config = ConfigManager(validate=False)
        print("✅ Configuration manager created successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration creation failed: {e}")
        return False

def test_config_access():
    """Test accessing configuration values."""
    try:
        print("🧪 Testing configuration value access...")
        from config import ConfigManager
        
        config = ConfigManager(validate=False)
        
        # Test getting API keys (should return dummy values)
        api_keys = config.get_api_keys()
        print(f"✅ API keys accessed: {len(api_keys)} keys found")
        
        # Test getting model config
        model_config = config.get_model_config()
        print(f"✅ Model config accessed: {model_config['default_llm_model']}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration access failed: {e}")
        return False

def main():
    """Run all configuration tests."""
    print("🔧 Configuration Import Test")
    print("=" * 30)
    
    tests = [
        ("Import", test_config_import),
        ("Creation", test_config_creation),
        ("Access", test_config_access)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Test Results")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! You can now run config_setup.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)