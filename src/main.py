import os
from src.feeds import Feeds
from src.raindrop import Raindrop
import datetime as dt
import feedparser


def main():
    # Load feeds
    feeds = Feeds("data/rainfeeds.opml")

    # Initialize Raindrop client wrapper
    raindrop_access_token = os.environ.get("RAINDROP_ACCESS_TOKEN")
    if raindrop_access_token is None:
        raise ValueError(
            "RAINDROP_ACCESS_TOKEN environment variable is not set")

    raindrop = Raindrop(raindrop_access_token)

    # Push new entries to Raindrop
    datetime_fmt = "%a, %d %b %Y %H:%M:%S %Z"

    for feed in feeds:
        now = dt.datetime.now(dt.timezone(dt.timedelta(0)))
        try:
            updated = dt.datetime.strptime(
                feeds[feed].get("updated"), datetime_fmt)
        except TypeError:
            updated = None

        entries = feedparser.parse(feed).entries
        new_entries = []

        for entry in entries:
            entry_published = dt.datetime(*entry["published_parsed"][:6])

            if updated is None or entry_published > updated:
                new_entries.append({
                    "published": entry_published.isoformat(),
                    "publisher": feeds[feed]["title"],
                    "category": feeds[feed].get("category", "Unsorted"),
                    "link": entry["link"]
                })

        raindrop.create_raindrops(new_entries)

        feeds[feed]["updated"] = now.strftime(datetime_fmt)


if __name__ == "__main__":
    main()
