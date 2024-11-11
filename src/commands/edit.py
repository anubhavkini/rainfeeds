import logging
from src.feeds import Feeds


def execute(args):
    logging.info("Loading subscription data.")
    feeds = Feeds("data/rainfeeds.opml")

    logging.info("Editing feed in subscription data.")
    feeds.edit(args.url, args.title, args.category)
