import logging
from src.feeds import Feeds


def execute(args):
    logging.info("Loading subscription data.")
    feeds = Feeds("data/rainfeeds.opml")

    logging.info("Listing feeds in subscription data.")
    feeds.list()
