from src.feeds import Feeds


def execute(args):
    # Load feeds
    feeds = Feeds("data/rainfeeds.opml")

    feeds.edit(args.url, args.title, args.category)
