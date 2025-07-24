# Security Guide for AI Telegram Bot 🔒

## Overview

This guide covers security best practices for your Telegram bot, focusing on protecting API keys, user data, and maintaining secure deployment practices.

## 🔑 API Key Security

### Never Commit Secrets to Git

**❌ NEVER do this:**
```python
# DON'T put secrets directly in code
TELEGRAM_BOT_TOKEN = "123456789:EXAMPLE_FAKE_TOKEN_DO_NOT_USE"
OPENAI_API_KEY = "sk-proj-EXAMPLE_FAKE_KEY_DO_NOT_USE_123456789"
```

**✅ Always do this:**
```python
# Use environment variables
import os
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

### Environment Variable Best Practices

1. **Use `.env` files for local development:**
   ```bash
   # .env file (never commit this!)
   TELEGRAM_BOT_TOKEN=your_actual_token_here
   OPENAI_API_KEY=your_actual_key_here
   ```

2. **Always include `.env` in `.gitignore`:**
   ```gitignore
   # Environment variables and secrets
   .env
   .env.*
   !.env.example
   ```

3. **Provide `.env.example` template:**
   ```bash
   # .env.example (safe to commit)
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Platform-Specific Security

#### Render Deployment
- Set environment variables in Render dashboard
- Never include secrets in `render.yaml`
- Use Render's secure environment variable storage

#### GitHub Actions (if using)
- Use GitHub Secrets for CI/CD
- Never log environment variables
- Use `secrets.TOKEN_NAME` in workflows

#### Heroku (alternative platform)
- Use `heroku config:set` for environment variables
- Enable automatic certificate management

## 🛡️ General Security Practices

### 1. Token Rotation

**Telegram Bot Token:**
- Rotate tokens if compromised
- Use BotFather's `/revoke` command if needed
- Monitor bot usage for suspicious activity

**OpenAI API Key:**
- Rotate keys monthly or quarterly
- Set usage limits in OpenAI dashboard
- Monitor API usage for unexpected spikes

### 2. Access Control

```python
# Example: Admin-only commands
ADMIN_USER_IDS = [12345678, 87654321]  # Load from env in production

async def admin_only_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("⚠️ This command is for administrators only.")
        return
    # Admin command logic here
```

### 3. Rate Limiting and Abuse Prevention

```python
# Enhanced rate limiting
class SecurityManager:
    def __init__(self):
        self.user_message_count = {}
        self.blocked_users = set()
        self.suspicious_patterns = [
            r'(api[_-]?key|token|secret)',
            r'(password|pwd|pass)',
            r'(hack|exploit|vulnerability)'
        ]
    
    def is_user_blocked(self, user_id: int) -> bool:
        return user_id in self.blocked_users
    
    def check_message_for_threats(self, message: str) -> bool:
        import re
        for pattern in self.suspicious_patterns:
            if re.search(pattern, message.lower()):
                return True
        return False
```

### 4. Input Validation

```python
def validate_user_input(message: str) -> bool:
    """Validate user input to prevent injection attacks"""
    if len(message) > 4000:  # Prevent extremely long messages
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
    for pattern in suspicious_patterns:
        if pattern.lower() in message.lower():
            return False
    
    return True
```

## 📊 Monitoring and Alerting

### 1. Usage Monitoring

```python
import logging
from datetime import datetime

# Enhanced logging
logger = logging.getLogger(__name__)

def log_security_event(event_type: str, user_id: int, details: str):
    """Log security-related events"""
    logger.warning(f"SECURITY: {event_type} - User: {user_id} - Details: {details}")
    
    # Optional: Send to external monitoring service
    # send_to_monitoring_service(event_type, user_id, details)
```

### 2. Error Handling Without Information Disclosure

```python
async def safe_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors without exposing sensitive information"""
    
    # Log detailed error for developers
    logger.error(f"Error for user {update.effective_user.id}: {context.error}")
    
    # Send generic message to user
    await update.message.reply_text(
        "🙏 I apologize, but I encountered a technical difficulty. "
        "Please try again in a moment."
    )
```

## 🔍 Security Checklist

### Before Deployment

- [ ] All secrets are in environment variables
- [ ] `.env` file is in `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] Rate limiting is implemented
- [ ] Input validation is in place
- [ ] Error handling doesn't expose sensitive data
- [ ] Logging is configured properly
- [ ] Admin access controls are implemented

### During Development

- [ ] Never commit `.env` files
- [ ] Use `.env.example` for templates
- [ ] Regularly rotate API keys
- [ ] Monitor API usage
- [ ] Test with dummy credentials first
- [ ] Use version control properly

### After Deployment

- [ ] Monitor bot usage patterns
- [ ] Check logs regularly for suspicious activity
- [ ] Keep dependencies updated
- [ ] Monitor API costs
- [ ] Have incident response plan ready

## 🚨 Incident Response

### If API Keys Are Compromised

1. **Immediate Actions:**
   ```bash
   # Rotate Telegram bot token
   # 1. Contact @BotFather
   # 2. Use /revoke command
   # 3. Generate new token
   
   # Rotate OpenAI API key
   # 1. Go to OpenAI platform
   # 2. Revoke compromised key
   # 3. Generate new key
   ```

2. **Update Deployment:**
   - Update environment variables on hosting platform
   - Redeploy application with new keys
   - Monitor for continued unauthorized usage

3. **Investigation:**
   - Check git history for accidentally committed secrets
   - Review access logs
   - Identify how keys were compromised
   - Implement additional security measures

### If Suspicious Activity Detected

```python
async def handle_suspicious_activity(user_id: int, activity_type: str):
    """Handle suspicious user activity"""
    
    # Log the incident
    logger.warning(f"Suspicious activity: {activity_type} from user {user_id}")
    
    # Temporarily block user
    blocked_users.add(user_id)
    
    # Optional: Alert administrators
    await notify_admins(f"Suspicious activity detected from user {user_id}")
    
    # Optional: Require re-authentication
    user_sessions.pop(user_id, None)
```

## 🔧 Security Configuration Examples

### Secure Configuration File

```python
# security_config.py
import os
from typing import List, Dict

class SecurityConfig:
    # Rate limiting
    MAX_MESSAGES_PER_MINUTE = 10
    COOLDOWN_DURATION = 3  # seconds
    
    # Admin settings
    ADMIN_USER_IDS: List[int] = [
        int(id) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id.strip()
    ]
    
    # Monitoring
    ENABLE_DETAILED_LOGGING = os.getenv('ENABLE_DETAILED_LOGGING', 'false').lower() == 'true'
    LOG_USER_MESSAGES = os.getenv('LOG_USER_MESSAGES', 'false').lower() == 'true'
    
    # API limits
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
```

### Environment Variables Template

```bash
# .env.example - Security-focused template

# Required API credentials
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here

# Security settings
ADMIN_USER_IDS=123456789,987654321
MAX_MESSAGES_PER_MINUTE=10
ENABLE_DETAILED_LOGGING=false
LOG_USER_MESSAGES=false

# API limits
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Optional: External monitoring
MONITORING_WEBHOOK_URL=
ALERT_EMAIL=
```

## 📚 Additional Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Telegram Bot API Security](https://core.telegram.org/bots/api#making-requests)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Python Security Best Practices](https://python.org/dev/security/)

---

**Remember: Security is an ongoing process, not a one-time setup. Stay vigilant and keep your security practices updated! 🛡️**
