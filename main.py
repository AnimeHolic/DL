import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.utils import helpers

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command to remove deleted accounts
def remove_deleted_accounts(update: Update, context: CallbackContext):
    # Check if the user is an admin
    if not context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id).status in ['administrator', 'creator']:
        update.message.reply_text("You need to be an admin to use this command.")
        return

    # Get the chat members
    members = context.bot.get_chat_members(update.effective_chat.id)
    
    deleted_count = 0
    for member in members:
        if member.user.is_deleted:
            context.bot.kick_chat_member(update.effective_chat.id, member.user.id)
            deleted_count += 1

    update.message.reply_text(f"Removed {deleted_count} deleted accounts from the group.")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /remove_deleted to remove deleted accounts.")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("7868318183:AAHUhX19qeUq5lmR6HAPwijKBoP-jHF8quI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("remove_deleted", remove_deleted_accounts))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
