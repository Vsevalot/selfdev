import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
from typing import List
from time import sleep

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def track76(update, context):
    station_url = "https://yandex.ru/maps/54/yekaterinburg/stops/stop__9811131"
    minutes_to_bus = get_time_to_bus(station_url)
    while minutes_to_bus < 0:
        sleep(60)
        minutes_to_bus = get_time_to_bus(station_url)

    update.message.reply_text(f"{minutes_to_bus} till 76 bus")

def get_time_to_bus(url: str, bnumber: str = "76") -> int:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    bus_list = BeautifulSoup(response.content, "html.parser").find("ul",
                                                                   class_="masstransit-brief-schedule-view__vehicles")
    buses: List[BeautifulSoup] = bus_list.find_all("li", class_="masstransit-vehicle-snippet-view _clickable")
    for bus in buses:
        bus_number = bus.find('a', class_="masstransit-vehicle-snippet-view__name").get_text().strip()
        if bus_number == bnumber:
            time_to_station = bus.find("span", class_="masstransit-prognoses-view__title-text").get_text().strip()
            if "каждые" in time_to_station:
                return -1
            else:
                minutes = time_to_station.split(' ')[0]
                return int(minutes)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    path_to_token = "token.txt"
    token = open(path_to_token, 'r').read()
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("track76", track76))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
