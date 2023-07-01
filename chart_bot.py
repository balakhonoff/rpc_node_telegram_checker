import telegram
from telegram.ext import Updater, CommandHandler, Filters
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import io

ALLOWED_USERS = ['my_telegram_username', 'someone_else']
OBJECT_OF_CHECKING = 'https://polygon-mainnet.chainstacklabs.com'

THRESHOLD = 5
LOG_FILE = '../logs.csv'


def send_pics(update, context, interval):

    try:
        user = update.effective_user
        if user.is_bot:
            return
        username = str(user.username)
        if username not in ALLOWED_USERS:
            return
    except Exception as e:
        print(repr(e))
        return

    df = pd.read_csv(LOG_FILE, header=None, names=[
        'timestamp_string', 'max_val', 'max_support', 'med_val', 'med_support', 'block_number'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp_string'])

    now = datetime.datetime.now()
    if interval == 'week':
        one_x_ago = now - datetime.timedelta(weeks=1)
    elif interval == 'day':  # day
        one_x_ago = now - datetime.timedelta(days=1)
    else:
        one_x_ago = now - datetime.timedelta(hours=1)

    df = df[df['timestamp'] >= one_x_ago]

    cols_to_show = ['node_lag', 'best_node_lag']
    df['node_lag'] = df['block_number'] - df['med_val']
    df['best_node_lag'] = df['max_val'] - df['med_val']

    plt.figure()
    sns.set(rc={'figure.figsize': (11, 4)})  # set figure size
    sns.lineplot(x='timestamp', y='value', hue='variable', data=df[['timestamp']+cols_to_show].melt('timestamp', var_name='variable', value_name='value'))
    plt.axhline(y=THRESHOLD, color='black', linestyle='--')
    plt.axhline(y=-THRESHOLD, color='black', linestyle='--')

    # Save the plot as an image file
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Send the plot as a photo using the Telegram bot API
    context.bot.send_photo(chat_id=user.id, photo=buf)

    # Close the plot to avoid memory leaks
    plt.close()


def hour(update, context):
    send_pics(update, context, 'hour')

def day(update, context):
    send_pics(update, context, 'day')

def week(update, context):
    send_pics(update, context, 'week')


token = "xxx"

bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler("hour", hour, filters=Filters.chat_type.private))
dispatcher.add_handler(CommandHandler("day", day, filters=Filters.chat_type.private))
dispatcher.add_handler(CommandHandler("week", week, filters=Filters.chat_type.private))

updater.start_polling()