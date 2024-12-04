import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ChatMemberHandler
from telegram.error import TelegramError

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "7868318183:AAHUhX19qeUq5lmR6HAPwijKBoP-jHF8quI"
BOT_OWNER_USER_ID = 6053231890  # Replace this with your own Telegram user ID
chat_ids = set()

async def add_chat(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    if chat and chat.type in ["group", "supergroup", "channel"]:
        chat_ids.add(chat.id)
        logger.info(f"Bot added to chat {chat.title} ({chat.id})")

async def remove_deleted_accounts(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.from_user.id == BOT_OWNER_USER_ID:
        for chat_id in chat_ids:
            try:
                chat = await context.bot.get_chat(chat_id)
                members = await context.bot.get_chat_administrators(chat_id)
                for member in members:
                    if member.user.is_deleted:
                        try:
                            await context.bot.ban_chat_member(chat_id, member.user.id)
                            await context.bot.unban_chat_member(chat_id, member.user.id)
                            logger.info(f'Removed deleted account: {member.user.id} from chat {chat.title}')
                        except Exception as e:
                            logger.error(f'Failed to remove deleted account from chat {chat.title}: {e}')
            except Exception as e:
                logger.error(f'Error checking chat {chat_id}: {e}')
        await update.message.reply_text("Checked and removed all deleted accounts from all managed groups and channels.")
    else:
        if update.message:
            await update.message.reply_text("You are not authorized to use this command.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", add_chat))
    application.add_handler(CommandHandler("remove_deleted", remove_deleted_accounts))
    application.add_handler(ChatMemberHandler(add_chat, ChatMemberHandler.MY_CHAT_MEMBER))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
