import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import asyncio

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot
async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'Hello {user.mention_html()}! Welcome to SPACERUN3008. Use /play to start the game!',
    )

# Command to trigger game start
async def play(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Start Game", callback_data='start_game')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ready to play? Click below to start!', reply_markup=reply_markup)

# Handler for the start game callback
async def start_game(update: Update, context):
    # Send game start prompt (redirect or actual game interface)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("The game is starting! Ready your space ship!")
    # You can link here to the game using the game URL
    game_url = "https://t.me/GAMES4PUNKSBOT?game=SPACERUN3008"
    await update.callback_query.message.reply_text(f"Click here to start playing: {game_url}")

# Error handler
def error(update: Update, context):
    logger.warning(f"Update {update} caused error {context.error}")

# Main function to run the bot
async def main():
    # Get the bot token from environment variables or GitHub secrets
    bot_token = os.getenv('BOT_TOKEN')  # Make sure to store this securely in GitHub secrets

    # Create the application
    application = ApplicationBuilder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))

    # Add callback query handlers
    application.add_handler(CallbackQueryHandler(start_game, pattern='start_game'))

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    await application.run_polling()

# Running the bot
if __name__ == '__main__':
    asyncio.run(main())
