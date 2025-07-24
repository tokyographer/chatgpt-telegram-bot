# Deployment Guide for AI Telegram Bot

## Overview

This guide covers deploying your AI Telegram Bot to Render, a cloud platform that makes it easy to deploy applications.

## Pre-deployment Checklist

### 1. Get Your Tokens

**Telegram Bot Token:**
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "AI Assistant Bot")
4. Choose a username (must end in 'bot', e.g., "ai_assistant_bot")
5. Copy the token provided (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

**OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Name your key (e.g., "Telegram Bot")
5. Copy the key (format: `sk-...`)

### 2. Test Locally (Optional but Recommended)

```bash
# Clone your repository
git clone <your-repo-url>
cd telegram-bot

# Copy environment template
cp .env.example .env

# Edit .env with your actual tokens
nano .env  # or use any text editor

# Test the bot
python test_setup.py

# Run the bot locally
python bot.py
```

## Deployment on Render

### Method 1: Automatic Deployment (Recommended)

1. **Fork the Repository**
   - Fork this repository to your GitHub account
   - Make sure it's public or you have a paid GitHub account

2. **Connect to Render**
   - Go to [Render.com](https://render.com)
   - Sign up/in with your GitHub account
   - Click "New +" → "Web Service"

3. **Connect Repository**
   - Connect your GitHub account if not already connected
   - Select your forked repository
   - Render will detect the `render.yaml` file automatically

4. **Configure Environment Variables**
   - In the Render dashboard, go to your service
   - Go to "Environment" tab
   - Add these variables:
     ```
     TELEGRAM_BOT_TOKEN=your_actual_telegram_token_here
     OPENAI_API_KEY=your_actual_openai_key_here
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your bot
   - Wait for deployment to complete (usually 2-3 minutes)

### Method 2: Manual Configuration

If you prefer manual setup:

1. **Create New Web Service**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your repository

2. **Configure Build Settings**
   - **Name**: `ai-assistant-bot` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

3. **Add Environment Variables**
   - Add `TELEGRAM_BOT_TOKEN` with your bot token
   - Add `OPENAI_API_KEY` with your OpenAI key

4. **Deploy**
   - Click "Create Web Service"
   - Monitor the build logs for any issues

## Post-Deployment

### 1. Verify Deployment

- Check the Render logs to ensure the bot started successfully
- Look for messages like:
  ```
  AIBot initialized successfully
  Bot is running with polling...
  ```

### 2. Test Your Bot

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. Try asking a question

### 3. Monitor Performance

- Check Render logs regularly
- Monitor your OpenAI usage at [OpenAI Platform](https://platform.openai.com/usage)
- Check for any error messages in the logs

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check environment variables are set correctly
- Verify tokens are valid
- Check Render logs for errors

**OpenAI API errors:**
- Verify your OpenAI API key
- Check your OpenAI account has credits
- Ensure you're using the correct model name

**Build failures:**
- Check `requirements.txt` for correct package versions
- Verify Python version compatibility
- Check Render build logs for specific errors

### Useful Commands

**Check bot status locally:**
```bash
python test_setup.py
```

**View Render logs:**
- Go to your service dashboard on Render
- Click "Logs" tab
- Use filters to find specific issues

**Update deployment:**
- Push changes to your GitHub repository
- Render will automatically redeploy

## Cost Considerations

### Render Costs
- **Free tier**: 750 hours/month (sufficient for most bots)
- **Paid tier**: $7/month for 24/7 uptime

### OpenAI Costs
- **GPT-4**: ~$0.03 per 1K tokens input, ~$0.06 per 1K tokens output
- **Typical conversation**: 100-500 tokens (~$0.003-0.03 per response)
- **Monthly estimate**: $5-50 depending on usage

### Cost Optimization Tips
1. Use GPT-3.5-turbo instead of GPT-4 for lower costs
2. Implement user limits or premium features
3. Monitor usage via OpenAI dashboard
4. Use Render's sleep feature for low-traffic periods

## Advanced Configuration

### Custom Domain (Paid Feature)
1. Purchase a domain
2. In Render dashboard, go to "Settings"
3. Add custom domain
4. Update DNS settings as instructed

### Monitoring and Alerts
1. Set up health checks in Render
2. Configure email alerts for service issues
3. Monitor logs regularly

### Scaling
- Render automatically handles basic scaling
- For high traffic, consider upgrading to paid plans
- Monitor response times and adjust as needed

## Security Best Practices

1. **Never commit API keys** to your repository
2. **Use environment variables** for all sensitive data
3. **Regularly rotate** your API keys
4. **Monitor usage** for unexpected activity
5. **Keep dependencies updated** for security patches

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Render and OpenAI documentation
3. Check the project's GitHub issues
4. Contact support if needed

## Maintenance

### Regular Tasks
- Monitor logs weekly
- Check OpenAI usage monthly
- Update dependencies quarterly
- Review and rotate API keys annually

### Updates
- Pull updates from the main repository
- Test changes locally before deploying
- Monitor after deployment for issues

---

**May your deployment be smooth and your bot serve users effectively! 🚀**
