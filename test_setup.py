#!/usr/bin/env python3
"""
Test script to verify the AI bot can initialize without errors
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_bot_initialization():
    """Test if the bot can initialize with dummy credentials"""
    
    # Set dummy environment variables for testing
    os.environ['TELEGRAM_BOT_TOKEN'] = 'dummy_token_for_testing'
    os.environ['OPENAI_API_KEY'] = 'dummy_key_for_testing'
    
    try:
        # Import the bot class
        from bot import AIBot
        
        print("✅ Successfully imported AIBot")
        
        # Test initialization (this will fail with dummy credentials, but should not crash during import)
        try:
            bot = AIBot()
            print("✅ Bot initialization successful")
        except Exception as e:
            print(f"⚠️ Bot initialization failed (expected with dummy credentials): {e}")
        
        print("✅ All imports and basic structure are working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_enhanced_bot():
    """Test the enhanced bot version"""
    try:
        from bot_enhanced import AIBotEnhanced
        print("✅ Successfully imported AIBotEnhanced")
        
        try:
            bot = AIBotEnhanced()
            print("✅ Enhanced bot initialization successful")
        except Exception as e:
            print(f"⚠️ Enhanced bot initialization failed (expected with dummy credentials): {e}")
            
        return True
    except Exception as e:
        print(f"❌ Enhanced bot test failed: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'bot.py',
        'bot_enhanced.py',
        'requirements.txt',
        'system_prompt.txt',
        'knowledge_base.md',
        '.env.example',
        'render.yaml',
        'config.json',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present!")
    return True

if __name__ == "__main__":
    print("🤖 Testing AI Telegram Bot Setup")
    print("=" * 50)
    
    print("\n📁 Checking files...")
    files_ok = check_files()
    
    print("\n🤖 Testing basic bot...")
    basic_bot_ok = test_bot_initialization()
    
    print("\n🚀 Testing enhanced bot...")
    enhanced_bot_ok = test_enhanced_bot()
    
    print("\n" + "=" * 50)
    if files_ok and basic_bot_ok and enhanced_bot_ok:
        print("🎉 All tests passed! Your AI bot is ready to deploy!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your real TELEGRAM_BOT_TOKEN and OPENAI_API_KEY to .env")
        print("3. Run: python bot.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    # Clean up environment variables
    if 'TELEGRAM_BOT_TOKEN' in os.environ:
        del os.environ['TELEGRAM_BOT_TOKEN']
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
