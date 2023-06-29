import telegram
from telegram.ext import Updater, CommandHandler, Filters

from functions import get_last_block_once, check_service

ALLOWED_USERS = ['my_telegram_username', 'someone_else']
OBJECT_OF_CHECKING = 'https://polygon-mainnet.chainstacklabs.com'
THRESHOLD = 5

def start(update, context):
    """Send a message when the command /start is issued."""
    try:
        # get user
        user = update.effective_user

        # filter bots
        if user.is_bot:
            return

        # check if the user is in the list of allowed users
        username = str(user.username)
        if username not in ALLOWED_USERS:
            return
    except Exception as e:
        print(f'{repr(e)}')
        return

    max_val, max_support, med_val, med_support = check_service()
    last_block = get_last_block_once(OBJECT_OF_CHECKING)

    message = ""
    message += f"Public median block number {med_val} (on {med_support}) RPCs\n"
    message += f"Public maximum block number +{max_val - med_val} (on {max_support}) PRCs\n"

    if last_block is not None:
        out_text = str(last_block - med_val) if last_block - med_val < 0 else '+' + str(last_block - med_val)

        if abs(last_block - med_val) > THRESHOLD:
            message += f"The node block number shift ⚠️<b>{out_text}</b>⚠️"
        else:
            message += f"The node block number shift {out_text}"
    else:
        message += f"The node has ⚠️<b>not responded</b>⚠️"

    context.bot.send_message(chat_id=user.id, text=message, parse_mode="HTML")


token = "xxx"

# set up the bot
bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# bind the handler function
dispatcher.add_handler(CommandHandler("start", start, filters=Filters.chat_type.private))

# run the bot
updater.start_polling()