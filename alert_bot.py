import telegram
from telegram.ext import Updater
from functions import get_last_block_once, check_service

OBJECT_OF_CHECKING = 'https://polygon-mainnet.chainstacklabs.com'

THRESHOLD = 5
USER_ID = 123456789

token = "xxx"


def check_for_alert(context):

    max_val, max_support, med_val, med_support = check_service()
    last_block = get_last_block_once(OBJECT_OF_CHECKING)

    message = ""
    message += f"Public median block number {med_val} (on {med_support}) RPCs\n"
    message += f"Public maximum block number +{max_val - med_val} (on {max_support}) PRCs\n"

    to_send = False

    if last_block is not None:
        out_text = str(last_block - med_val) if last_block - med_val < 0 else '+' + str(last_block - med_val)

        if abs(last_block - med_val) > THRESHOLD:
            to_send = True
            message += f"The node block number shift ⚠️<b>{out_text}</b>⚠️"
        else:
            message += f"The node block number shift {out_text}"
    else:
        to_send = True
        message += f"The node has ⚠️<b>not responded</b>⚠️"

    if to_send:
        context.bot.send_message(chat_id=USER_ID, text=message, parse_mode="HTML")


bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue
job_queue.run_repeating(check_for_alert, interval=10.0 * 60.0, first=0.0)

updater.start_polling()