import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# Configuration - YOUR BOT TOKEN
BOT_TOKEN = "8071872909:AAEcC5N51y6n1rxVeKsPpqurb5ZMse69Qdg"

# Social Media Links (Replace with your actual links)
SOCIAL_LINKS = {
    "channel": "https://t.me/your_channel",
    "group": "https://t.me/your_group",
    "twitter": "https://twitter.com/your_twitter",
    "facebook": "https://facebook.com/your_facebook"
}

# Fake SOL addresses for transaction simulation
FAKE_TX_IDS = [
    "5gY2783hD8k9fJ7s6K5l4M3n2B1v9C8x0Z",
    "7sP6k9Lm3nBz2Vx8cFt0JyHaQwD5rT4eXg",
    "9Qw2E4r6T8y1U3i5O7p0AaSd9Fg7H8j2Kl",
    "3MjK9L0pO8iU7y6T5r4E1w2Q9a8S5d4F7g",
    "Xc8V9bN7m6K5j4H3g2F1d0Sa9Q8w7E4rT"
]

# Conversation state
GET_WALLET = 1

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_fake_tx_id():
    """Generate a fake Solana transaction ID"""
    prefix = random.choice(FAKE_TX_IDS)
    suffix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
    return f"{prefix}{suffix}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with instructions"""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=SOCIAL_LINKS['channel'])],
        [InlineKeyboardButton("👥 Join Group", url=SOCIAL_LINKS['group'])],
        [InlineKeyboardButton("🐦 Follow Twitter", url=SOCIAL_LINKS['twitter'])],
        [InlineKeyboardButton("📘 Follow Facebook", url=SOCIAL_LINKS['facebook'])],
        [InlineKeyboardButton("✅ I've Completed All Tasks", callback_data="submit")]
    ]
    
    await update.message.reply_text(
        f"🌟 *Welcome {user.first_name} to CryptoWeatStudio Airdrop!* 🌟\n\n"
        "🎁 **Claim 100 SOL Instantly!**\n\n"
        "Complete these simple steps:\n"
        "1. ➡️ Join our Telegram Channel\n"
        "2. 👥 Join our Telegram Group\n"
        "3. 🐦 Follow us on Twitter\n"
        "4. 👍 Follow us on Facebook\n\n"
        "After completing all tasks, click the button below to claim your reward:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the submission callback"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎉 *Tasks Completed!* 🎉\n\n"
        "Please send your Solana wallet address now:\n"
        "(Example: `7sP6k9Lm3nBz2Vx8cFt0Jy...`)\n\n"
        "💡 _We trust you completed all tasks honestly!_ 😊",
        parse_mode="Markdown"
    )
    return GET_WALLET

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive wallet address and send confirmation"""
    wallet = update.message.text.strip()
    user = update.message.from_user
    
    # Simple SOL address validation
    if len(wallet) < 20 or not wallet.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
        await update.message.reply_text(
            "⚠️ *Invalid Solana address format!*\n"
            "Please send a valid Solana wallet address (should be at least 20 characters and start with a number):",
            parse_mode="Markdown"
        )
        return GET_WALLET
    
    # Generate fake transaction details
    tx_id = generate_fake_tx_id()
    explorer_url = f"https://explorer.solana.com/tx/{tx_id}"
    
    # Send congratulations message
    await update.message.reply_text(
        f"🎉 *CONGRATULATIONS {user.first_name}!* 🎉\n\n"
        "You've successfully qualified for the CryptoWeatStudio Airdrop!\n\n"
        f"💸 *100 SOL has been sent to:*\n`{wallet}`\n\n"
        f"📄 *Transaction ID:*\n`{tx_id}`\n"
        f"🔍 [View on Solana Explorer]({explorer_url})\n\n"
        "⏱️ *Estimated Confirmation:* 10 seconds\n\n"
        "🎉 *Thank you for participating!*\n"
        "Hope you didn't cheat the system 😉\n\n"
        "⚠️ *Note:* This is a test bot - no actual SOL has been sent",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    # Log the submission
    logger.info(f"New airdrop claim: User {user.id} | Wallet: {wallet}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text(
        "🚫 Operation cancelled. Use /start to begin again."
    )
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show fake statistics"""
    fake_count = random.randint(500, 1000)
    await update.message.reply_text(
        f"📊 *CryptoWeatStudio Airdrop Stats*\n\n"
        f"👥 Total Participants: {fake_count}\n"
        f"💸 SOL Distributed: {fake_count * 100} SOL\n"
        f"⏰ Time Remaining: 12 hours\n\n"
        "Use /start to participate!",
        parse_mode="Markdown"
    )

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_submission, pattern="^submit$"))
    application.add_handler(CommandHandler('stats', stats))
    
    # Start the Bot
    logger.info("Starting CryptoWeatStudio Airdrop Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
