import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# Configuration
TOKEN = "8071872909:AAEcC5N51y6n1rxVeKsPpqurb5ZMse69Qdg"
CHANNEL_LINK = "https://t.me/your_channel"
GROUP_LINK = "https://t.me/your_group"
TWITTER_LINK = "https://twitter.com/your_twitter"
FACEBOOK_LINK = "https://facebook.com/your_facebook"

# Conversation states
GET_WALLET = 1

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with instructions"""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("📘 Follow Facebook", url=FACEBOOK_LINK)],
        [InlineKeyboardButton("✅ I've Completed All Tasks", callback_data="submit")]
    ]
    
    await update.message.reply_text(
        f"👋 *Welcome {user.first_name} to CryptoWeatStudio Airdrop!*\n\n"
        "To qualify for the airdrop, please complete these steps:\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow us on Twitter\n"
        "4. Follow us on Facebook\n\n"
        "After completing all tasks, click the button below to submit your wallet address:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the submission callback"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎉 *Tasks Completed!*\n\n"
        "Please send your Solana wallet address now:\n"
        "(Example: `7sP6...`)\n\n"
        "_We trust you completed all tasks honestly!_ 😊",
        parse_mode="Markdown"
    )
    return GET_WALLET

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive wallet address and send confirmation"""
    wallet = update.message.text.strip()
    user = update.message.from_user
    
    # Simple SOL address validation
    if len(wallet) < 30 or not wallet.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        await update.message.reply_text(
            "⚠️ *Invalid Solana address format!*\n"
            "Please send a valid Solana wallet address:",
            parse_mode="Markdown"
        )
        return GET_WALLET
    
    # Send congratulations message
    await update.message.reply_text(
        f"🚀 *CONGRATULATIONS {user.first_name}!*\n\n"
        "You've successfully qualified for the CryptoWeatStudio Airdrop!\n\n"
        f"💸 *100 SOL has been sent to your address:*\n`{wallet}`\n\n"
        "Thank you for participating! Hope you didn't cheat the system 😉\n\n"
        "_Note: This is a testing bot, no actual SOL will be sent_",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text(
        "Operation cancelled. Use /start to begin again."
    )
    return ConversationHandler.END

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_submission, pattern="^submit$"))
    
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
