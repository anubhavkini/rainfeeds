import logging
from src.feeds import Feeds


def execute(args):
    logging.info("Loading subscription data.")
    feeds = Feeds("data/rainfeeds.opml")

    logging.info("Adding feed to subscription data.")
    feeds.add(args.url, args.title, args.category)
