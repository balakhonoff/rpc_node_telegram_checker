import datetime
import csv

from functions import get_last_block_once, check_service


LOG_FILE = '../logs.csv'
OBJECT_OF_CHECKING = 'https://polygon-mainnet.chainstacklabs.com'


def save_log(log_data):
    with open(LOG_FILE, mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(log_data)


if __name__ == '__main__':
    max_val, max_support, med_val, med_support = check_service()
    last_block = get_last_block_once(OBJECT_OF_CHECKING)

    timestamp_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_data = [timestamp_string, max_val, max_support, med_val, med_support, last_block]
    save_log(log_data)