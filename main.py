import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your bot token
TOKEN = '7868318183:AAHUhX19qeUq5lmR6HAPwijKBoP-jHF8quI'

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Hello! I am a bot that removes deleted accounts from the group.')

# Define a function to check and remove deleted accounts
def remove_deleted_accounts(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    try:
        members = bot.get_chat_administrators(chat_id)
        for member in members:
            user = member.user
            if user.is_deleted:
                bot.kick_chat_member(chat_id, user.id)
                update.message.reply_text(f'Removed deleted account: {user.id}')
    except Exception as e:
        logger.error(f'Error: {e}')
        update.message.reply_text('An error occurred while trying to remove deleted accounts.')

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('clean', remove_deleted_accounts))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl+C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
