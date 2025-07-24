#!/usr/bin/env python3
"""
Security check script to verify no secrets are exposed
"""

import os
import re
import glob
from pathlib import Path

def check_for_exposed_secrets():
    """Check for potentially exposed API keys and secrets in the codebase"""
    
    # Patterns that might indicate exposed secrets
    secret_patterns = [
        r'TELEGRAM_BOT_TOKEN\s*=\s*["\']?\d+:[A-Za-z0-9_-]+["\']?',
        r'OPENAI_API_KEY\s*=\s*["\']?sk-[a-zA-Z0-9-_]+["\']?',
        r'sk-proj-[a-zA-Z0-9-_]+',
        r'\d{8,10}:[A-Za-z0-9_-]{35}',  # Telegram bot token pattern
        r'sk-[a-zA-Z0-9]{48,}',  # OpenAI API key pattern (older format)
    ]
    
    # Files to check (excluding .env.example which should have placeholders)
    file_patterns = [
        '*.py',
        '*.md',
        '*.txt',
        '*.json',
        '*.yaml',
        '*.yml'
    ]
    
    print("🔍 Checking for exposed secrets...")
    
    issues_found = []
    
    for pattern in file_patterns:
        for filepath in glob.glob(pattern):
            if filepath in ['.env', '.env.local', '.env.production']:
                continue  # Skip actual env files
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for line_num, line in enumerate(content.split('\n'), 1):
                    for secret_pattern in secret_patterns:
                        if re.search(secret_pattern, line):
                            # Check if it's a placeholder
                            if ('your_' in line.lower() or 
                                'placeholder' in line.lower() or
                                'example' in line.lower() or
                                'dummy' in line.lower()):
                                continue
                                
                            issues_found.append({
                                'file': filepath,
                                'line': line_num,
                                'content': line.strip()[:50] + '...' if len(line.strip()) > 50 else line.strip()
                            })
                            
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
    
    if issues_found:
        print("❌ POTENTIAL SECURITY ISSUES FOUND:")
        for issue in issues_found:
            print(f"  📁 {issue['file']}:{issue['line']}")
            print(f"     🔍 {issue['content']}")
        print("\n🚨 ACTION REQUIRED:")
        print("1. Remove any real API keys from these files")
        print("2. Add the files to .gitignore if they contain secrets")
        print("3. Rotate any exposed API keys immediately")
        print("4. Check git history: git log --all -p | grep -i 'sk-\\|\\d\\+:[A-Za-z]'")
        
    else:
        print("✅ No obvious secrets found in tracked files!")
    
    # Check if .env file exists and warn about it
    if os.path.exists('.env'):
        print("\n⚠️  .env file detected - ensure it's in .gitignore")
        
    # Check .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' not in gitignore_content:
                print("❌ .env is not in .gitignore - add it immediately!")
            else:
                print("✅ .env is properly ignored in .gitignore")
    else:
        print("❌ No .gitignore file found - create one to protect secrets!")

def check_git_history():
    """Check if secrets might be in git history"""
    print("\n🔍 Checking git history for potential secrets...")
    
    try:
        import subprocess
        
        # Check for patterns that might be secrets in git history
        patterns = [
            r'sk-[a-zA-Z0-9-_]{20,}',
            r'\d{8,10}:[A-Za-z0-9_-]{30,}',
        ]
        
        for pattern in patterns:
            result = subprocess.run(
                ['git', 'log', '--all', '-p', '--grep=' + pattern],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"⚠️  Found potential secrets in git history matching pattern: {pattern}")
                print("   Consider using git-filter-branch or BFG Repo-Cleaner to clean history")
            
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Could not check git history: {e}")

if __name__ == "__main__":
    print("🔒 Security Check for AI Telegram Bot")
    print("=" * 40)
    
    check_for_exposed_secrets()
    check_git_history()
    
    print("\n📋 Security Checklist:")
    print("□ API keys are in environment variables only")
    print("□ .env file is in .gitignore")
    print("□ No secrets in code files")
    print("□ No secrets in git history")
    print("□ API keys are rotated regularly")
    print("□ Bot has rate limiting enabled")
    
    print("\n📚 For more security guidance, see SECURITY.md")
