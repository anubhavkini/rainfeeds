import os
from src.feeds import Feeds
from src.feed import FeedTracker
from src.raindrop import Raindrop


def main():
    # Load feeds
    feeds = Feeds("data/feeds_test.opml")

    # Create feed tracker
    feed_tracker = FeedTracker(feeds)

    # Initialize Raindrop client wrapper
    raindrop_access_token = os.environ.get("RAINDROP_ACCESS_TOKEN")
    if raindrop_access_token is None:
        raise ValueError(
            "RAINDROP_ACCESS_TOKEN environment variable is not set")

    raindrop = Raindrop(raindrop_access_token)

    # Push new items to Raindrop.io
    raindrop.create_raindrops(feeds.new_items())


if __name__ == "__main__":
    main()
