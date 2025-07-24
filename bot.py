import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI
from telegram import Update
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


class AIBot:
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
        
        # Load system prompt and knowledge base
        self.system_prompt = self.load_system_prompt()
        self.knowledge_base = self.load_knowledge_base()
        
        logger.info("AI Bot initialized successfully")

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
        if user_id in self.user_cooldowns:
            time_since_last = now - self.user_cooldowns[user_id]
            if time_since_last < self.cooldown_duration:
                return False
        
        self.user_cooldowns[user_id] = now
        return True

    async def get_openai_response(self, user_message: str) -> str:
        """Get response from OpenAI API"""
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
            
            logger.info(f"Making OpenAI API call for message: {user_message[:50]}...")
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info("OpenAI API call successful")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "I apologize, but I'm experiencing some technical difficulties at the moment. Please try again in a few moments."

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user = update.effective_user
        logger.info(f"Start command from user {user.id} ({user.username})")
        
        welcome_message = """🤖 Hello and welcome!

I'm your AI assistant, here to help you with questions, provide information, and assist with various tasks.

I can help you with:
• 📝 Answering questions and providing information
• 💡 Problem-solving and brainstorming
• 📚 Educational content and explanations
• 🔧 Technical guidance and support
• 💬 General conversation and assistance

Available commands:
/start - Begin our conversation
/help - Show detailed help information

Simply send me any question or message, and I'll do my best to help you!

Looking forward to assisting you! ✨"""
        
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        user = update.effective_user
        logger.info(f"Help command from user {user.id} ({user.username})")
        
        help_message = """🤖 How to interact with your AI assistant:

• Simply send me any text message with your question or request
• I can help with a wide variety of topics and tasks
• Ask follow-up questions to get more detailed information
• Be as specific as possible for the best results

Available commands:
/start - Welcome message and introduction
/help - Show this message

I'm here to help make your tasks easier and provide reliable information!

Ready to assist you! �"""
        
        await update.message.reply_text(help_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming text messages"""
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Message from user {user.id} ({user.username}): {message_text[:100]}...")
        
        # Check rate limiting
        if not self.check_rate_limit(user.id):
            await update.message.reply_text(
                "⏰ Please wait a moment between messages. "
                "This helps me provide better responses!"
            )
            return
        
        # Show typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get response from OpenAI
            response = await self.get_openai_response(message_text)
            
            # Send response
            await update.message.reply_text(response)
            logger.info(f"Response sent to user {user.id}")
            
        except Exception as e:
            logger.error(f"Error handling message from user {user.id}: {e}")
            await update.message.reply_text(
                "🤖 I apologize, but I encountered a technical issue. "
                "Please try again in a moment!"
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        """Run the bot"""
        logger.info("Starting AI Bot...")
        
        # Create application
        application = Application.builder().token(self.telegram_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Run the bot
        logger.info("Bot is running with polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main function"""
    try:
        bot = AIBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()
