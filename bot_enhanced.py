#!/usr/bin/env python3
"""
Enhanced AI Telegram Bot with additional features
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List

from dotenv import load_dotenv
from openai import AsyncOpenAI
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AIBotEnhanced:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
        
        # Rate limiting: user_id -> last_message_time
        self.user_cooldowns: Dict[int, datetime] = {}
        self.cooldown_duration = timedelta(seconds=3)  # 3 seconds cooldown
        
        # User stats tracking
        self.user_stats: Dict[int, dict] = {}
        
        # Load configuration
        self.config = self.load_config()
        self.system_prompt = self.load_system_prompt()
        self.knowledge_base = self.load_knowledge_base()
        
        logger.info("Enhanced AI Bot initialized successfully")

    def load_config(self) -> dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "openai_model": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.7,
            "cooldown_seconds": 3,
            "enable_stats": True,
            "enable_typing_indicator": True
        }
        
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info("Configuration loaded from config.json")
                return {**default_config, **config}
        except FileNotFoundError:
            logger.info("config.json not found, using default configuration")
            return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}, using defaults")
            return default_config

    def load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            with open('system_prompt.txt', 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
                logger.info("System prompt loaded successfully")
                return prompt
        except FileNotFoundError:
            logger.warning("system_prompt.txt not found, using default prompt")
            return self.get_default_system_prompt()
        except Exception as e:
            logger.error(f"Error loading system prompt: {e}")
            return self.get_default_system_prompt()

    def get_default_system_prompt(self) -> str:
        """Default system prompt if file is not available"""
        return """You are a helpful, knowledgeable AI assistant designed to provide thoughtful and accurate responses to user questions. You are friendly, professional, and adaptable to different conversation styles and topics.

Your responses should be:
- Clear and informative
- Helpful and supportive
- Professional yet approachable
- Tailored to the user's level of understanding
- Respectful and inclusive

When someone asks you a question, provide accurate and relevant information while maintaining a consistent and reliable personality. Be honest about your limitations and suggest ways users might find additional information when needed."""

    def load_knowledge_base(self) -> Optional[str]:
        """Load knowledge base from markdown file"""
        try:
            with open('knowledge_base.md', 'r', encoding='utf-8') as f:
                knowledge = f.read().strip()
                logger.info("Knowledge base loaded successfully")
                return knowledge
        except FileNotFoundError:
            logger.info("knowledge_base.md not found, continuing without external knowledge base")
            return None
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return None

    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limit"""
        now = datetime.now()
        cooldown = timedelta(seconds=self.config.get('cooldown_seconds', 3))
        
        if user_id in self.user_cooldowns:
            time_since_last = now - self.user_cooldowns[user_id]
            if time_since_last < cooldown:
                return False
        
        self.user_cooldowns[user_id] = now
        return True

    def update_user_stats(self, user_id: int, username: str = None):
        """Update user statistics"""
        if not self.config.get('enable_stats', True):
            return
            
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                'username': username,
                'first_interaction': datetime.now().isoformat(),
                'message_count': 0,
                'last_interaction': None
            }
        
        self.user_stats[user_id]['message_count'] += 1
        self.user_stats[user_id]['last_interaction'] = datetime.now().isoformat()
        if username:
            self.user_stats[user_id]['username'] = username

    async def get_openai_response(self, user_message: str, user_id: int = None) -> str:
        """Get response from OpenAI API with enhanced error handling"""
        try:
            # Construct the full prompt
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add knowledge base context if available
            if self.knowledge_base:
                knowledge_context = f"Additional context and knowledge:\n{self.knowledge_base}\n\nUser question: {user_message}"
                messages.append({"role": "user", "content": knowledge_context})
            else:
                messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Making OpenAI API call for user {user_id}, message: {user_message[:50]}...")
            
            response = await self.openai_client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-4'),
                messages=messages,
                max_tokens=self.config.get('max_tokens', 1000),
                temperature=self.config.get('temperature', 0.7)
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"OpenAI API call successful for user {user_id}")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error for user {user_id}: {e}")
            return self.get_fallback_response()

    def get_fallback_response(self) -> str:
        """Return a meaningful fallback response when OpenAI is unavailable"""
        fallback_responses = [
            "🤖 I apologize, but I'm experiencing some technical difficulties at the moment. Please try again in a few moments.",
            "⚠️ I'm currently having trouble connecting to my AI services. Please give me a moment and try again.",
            "� I'm experiencing a temporary service interruption. Please try your question again shortly."
        ]
        import random
        return random.choice(fallback_responses)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user = update.effective_user
        self.update_user_stats(user.id, user.username)
        logger.info(f"Start command from user {user.id} ({user.username})")
        
        welcome_message = """🤖 Hello and welcome!

I'm your enhanced AI assistant, here to help you with questions, provide information, and assist with various tasks.

I can help you with:
• 📝 Answering questions and providing information
• 💡 Problem-solving and brainstorming
• 📚 Educational content and explanations
• � Technical guidance and support
• � General conversation and assistance
• 📊 Data analysis and research
• ✍️ Writing and creative tasks

Available commands:
/start - Begin our conversation
/help - Show detailed help information
/about - Learn about this bot
/stats - Your interaction statistics (if enabled)

Simply send me any question or message, and I'll do my best to help you!

Looking forward to assisting you! ✨

*"Every question is an opportunity to learn something new."*"""
        
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        user = update.effective_user
        self.update_user_stats(user.id, user.username)
        logger.info(f"Help command from user {user.id} ({user.username})")
        
        help_message = """🤖 How to interact with your enhanced AI assistant:

**Asking Questions:**
• Simply send me any text message with your question
• I can help with a wide variety of topics and tasks
• Ask follow-up questions to get more detailed information
• Be as specific as possible for the best results

**What I can help with:**
• 📚 General knowledge and information
• 💡 Problem-solving and advice
• 🎓 Educational explanations and tutorials
• � Technical support and guidance
• ✍️ Writing and creative tasks
• � Data analysis and research
• 💬 General conversation and brainstorming
• � Personalized assistance based on your needs

**Available Commands:**
/start - Welcome message and introduction
/help - This detailed help message
/about - Information about this bot
/stats - Your personal interaction statistics

**Features:**
• Enhanced with user statistics tracking
• Configurable response parameters
• Multiple fallback responses for reliability
• Comprehensive logging for quality assurance

**Tips for best results:**
• Ask one question at a time for focused responses
• There's a brief cooldown between messages to ensure quality
• Feel free to ask for clarification or additional details
• Let me know if you need information explained differently

I'm here to help make your tasks easier and provide reliable, intelligent assistance!

Ready to help you achieve your goals! �"""
        
        await update.message.reply_text(help_message)

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /about command"""
        user = update.effective_user
        self.update_user_stats(user.id, user.username)
        logger.info(f"About command from user {user.id} ({user.username})")
        
        about_message = """🤖 **About Your Enhanced AI Assistant**

I am an advanced AI-powered assistant, created to provide intelligent, helpful, and reliable support for a wide variety of tasks and questions. Built with cutting-edge technology and designed for flexibility.

**My Purpose:**
To serve as your versatile digital companion, offering assistance, information, and support tailored to your specific needs and preferences.

**My Capabilities Include:**
• Advanced natural language understanding
• Comprehensive knowledge across many domains
• Customizable personality and expertise areas
• Intelligent conversation and context awareness
• Problem-solving and analytical thinking

**Technical Details:**
• Powered by OpenAI's advanced language models
• Enhanced with customizable knowledge base integration
• Designed for reliable, consistent performance
• Includes advanced features like user statistics and configuration options
• Built with security and privacy in mind

**My Approach:**
I strive to provide assistance that is:
- Accurate and well-informed
- Tailored to your communication style
- Respectful and professional
- Helpful for achieving your goals
- Honest about limitations

**Enhanced Features:**
This enhanced version includes user statistics tracking, configurable response parameters, and additional customization options for a more personalized experience.

**Remember:**
While I can provide information and assistance, critical decisions should always involve your own judgment and expertise. I'm here to support and enhance your capabilities, not replace your thinking.

*"Intelligence is not about having all the answers, but knowing how to find them."*

Created to empower and assist users in achieving their goals 🚀

Version: Enhanced Edition
Last updated: {datetime.now().strftime('%B %Y')}"""
        
        await update.message.reply_text(about_message)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /stats command"""
        user = update.effective_user
        user_id = user.id
        
        if not self.config.get('enable_stats', True):
            await update.message.reply_text("📊 Statistics tracking is currently disabled.")
            return
        
        self.update_user_stats(user_id, user.username)
        logger.info(f"Stats command from user {user_id} ({user.username})")
        
        if user_id in self.user_stats:
            stats = self.user_stats[user_id]
            first_interaction = datetime.fromisoformat(stats['first_interaction'])
            days_active = (datetime.now() - first_interaction).days + 1
            
            stats_message = f"""📊 **Your AI Assistant Statistics**

🤖 **Your Journey with the AI Assistant:**
• First interaction: {first_interaction.strftime('%B %d, %Y')}
• Days active: {days_active}
• Total messages: {stats['message_count']}
• Username: @{stats.get('username', 'Unknown')}

� **Progress:**
Every conversation helps improve our interaction and your experience with AI assistance.

*"Learning is a continuous journey of questions and discoveries."*

Keep exploring and asking questions! �"""
        else:
            stats_message = "📊 No statistics available yet. Start your journey by asking a question!"
        
        await update.message.reply_text(stats_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming text messages"""
        user = update.effective_user
        message_text = update.message.text
        user_id = user.id
        
        logger.info(f"Message from user {user_id} ({user.username}): {message_text[:100]}...")
        
        # Update user stats
        self.update_user_stats(user_id, user.username)
        
        # Check rate limiting
        if not self.check_rate_limit(user_id):
            remaining_time = self.config.get('cooldown_seconds', 3)
            await update.message.reply_text(
                f"🕰️ Please wait {remaining_time} seconds between messages. "
                "This helps ensure quality responses for everyone."
            )
            return
        
        # Show typing action if enabled
        if self.config.get('enable_typing_indicator', True):
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get response from OpenAI
            response = await self.get_openai_response(message_text, user_id)
            
            # Send response
            await update.message.reply_text(response)
            logger.info(f"Response sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error handling message from user {user_id}: {e}")
            await update.message.reply_text(
                "� I encountered a technical issue while processing your request. "
                "Please try again in a moment."
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

    async def setup_bot_commands(self, application: Application) -> None:
        """Set up bot commands menu"""
        commands = [
            BotCommand("start", "Start using the AI assistant"),
            BotCommand("help", "Get help and usage instructions"),
            BotCommand("about", "Learn about this AI assistant"),
            BotCommand("stats", "View your interaction statistics")
        ]
        
        await application.bot.set_my_commands(commands)
        logger.info("Bot commands menu set up successfully")

    def run(self):
        """Run the bot"""
        logger.info("Starting Enhanced AI Bot...")
        
        # Create application
        application = Application.builder().token(self.telegram_token).build()
        
        # Set up bot commands menu
        asyncio.create_task(self.setup_bot_commands(application))
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("about", self.about_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Run the bot
        logger.info("Enhanced Bot is running with polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main function"""
    try:
        bot = AIBotEnhanced()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()
