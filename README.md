# AI-Powered Telegram Bot 🤖

A versatile, customizable Telegram bot powered by OpenAI's GPT models. Create your own AI assistant with any personality, expertise, or knowledge base you desire. Perfect for businesses, communities, educational purposes, or personal projects.

## Features

- 🤖 **Telegram Integration**: Built with python-telegram-bot v20+
- 🧠 **AI-Powered Responses**: Uses OpenAI GPT-4 for intelligent conversations
- 📚 **Customizable Knowledge Base**: Load your own content and expertise
- 🎭 **Flexible Personality**: Easily customize the bot's character and tone
- 🔒 **Secure**: Environment-based configuration for API keys
- 📝 **Logging**: Comprehensive logging for messages, API calls, and errors
- ⏱️ **Rate Limiting**: Built-in cooldown mechanism to prevent spam
- 🚀 **Deploy Ready**: Configured for easy deployment on Render
- 🔄 **Async Support**: Fully asynchronous for optimal performance
- 🛠️ **Modular Design**: Easy to extend with new features and commands

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd telegram-bot
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your tokens:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Get Your Tokens

**Telegram Bot Token:**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided

**OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Copy the key

### 4. Run the Bot

```bash
python bot.py
```

## Project Structure

```
telegram-bot/
├── bot.py                 # Main bot application
├── bot_enhanced.py        # Enhanced version with extra features
├── system_prompt.txt      # Bot personality and instructions
├── knowledge_base.md      # Custom knowledge base content
├── config.json           # Configuration settings
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables (create this)
├── README.md             # This file
├── DEPLOYMENT.md         # Detailed deployment guide
├── SECURITY.md           # Security best practices and key protection
├── USAGE_EXAMPLES.md     # Examples for different use cases
├── test_setup.py         # Setup verification script
└── .gitignore           # Protects sensitive files and API keys
```

## Deployment on Render

### Automatic Deployment

1. Fork this repository to your GitHub account
2. Connect your GitHub account to [Render](https://render.com)
3. Create a new "Web Service" and connect your forked repository
4. Render will automatically detect the `render.yaml` configuration
5. Add your environment variables in the Render dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
6. Deploy!

### Manual Configuration

If you prefer manual setup:

1. Create a new "Web Service" on Render
2. Connect your repository
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Environment**: Python 3
4. Add environment variables in the dashboard
5. Deploy

## Bot Commands

- `/start` - Welcome message and introduction
- `/help` - Show available commands and usage instructions

## Customization

### Modify the Bot's Personality

Edit `system_prompt.txt` to change how the bot responds. You can create any type of assistant:
- **Customer Service**: Professional and helpful
- **Educational Tutor**: Patient and informative  
- **Creative Writing Assistant**: Imaginative and inspiring
- **Technical Support**: Knowledgeable and precise
- **Personal Coach**: Motivating and supportive

### Extend the Knowledge Base

Add your own content to `knowledge_base.md` to give the bot specialized knowledge:
- Company information and policies
- Product documentation
- Educational content
- FAQs and troubleshooting guides
- Industry-specific expertise

### Add New Features

The code is modular and easy to extend:

- Add new command handlers in the `run()` method
- Create new methods for different types of interactions
- Implement additional OpenAI models or parameters
- Add database integration for user history
- Integrate with external APIs or services

## Features Explained

### Rate Limiting
- 3-second cooldown between messages per user
- Prevents spam and manages API costs
- Graceful user feedback when rate limited

### Error Handling
- Comprehensive error logging
- Graceful fallbacks for API failures
- User-friendly error messages

### Logging
- All interactions logged to `bot.log`
- Console and file logging
- Includes timestamps and user information

### Security
- Environment variables for sensitive data
- No hardcoded API keys
- Proper error handling without exposing internal details
- Comprehensive `.gitignore` to protect secrets
- Rate limiting to prevent abuse

**🔒 Important Security Note:** 
Never commit your `.env` file or any files containing API keys to version control. See `SECURITY.md` for comprehensive security guidelines and best practices.

## Requirements

- Python 3.8+
- Telegram Bot Token
- OpenAI API Key
- Internet connection for API calls

## Dependencies

- `python-telegram-bot==20.8` - Telegram bot framework
- `openai==1.54.3` - OpenAI API client
- `python-dotenv==1.0.0` - Environment variable management

## Troubleshooting

### Bot doesn't respond
- Check that your tokens are correctly set in `.env`
- Verify the bot is running without errors in the console
- Ensure your OpenAI account has available credits

### Deployment issues on Render
- Check that environment variables are set in Render dashboard
- Review the build logs for any dependency issues
- Ensure your repository is public or properly connected

### Rate limiting too strict
- Modify `self.cooldown_duration` in `bot.py`
- Adjust the cooldown period as needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs in `bot.log`
3. Open an issue on GitHub with details about your problem

---

*Happy coding and building amazing AI experiences! 🚀*
