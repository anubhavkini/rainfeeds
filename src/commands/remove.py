import logging
from src.feeds import Feeds


def execute(args):
    logging.info("Loading subscription data.")
    feeds = Feeds("data/rainfeeds.opml")

    logging.info("Removing feed from subscription data.")
    feeds.remove(args.url)
