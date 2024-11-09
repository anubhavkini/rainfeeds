from src.feeds import Feeds


def execute(args):
    # Load feeds
    feeds = Feeds("data/rainfeeds.opml")

    feeds.remove(args.url)
