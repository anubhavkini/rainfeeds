import os
import sys
import logging
from src.feeds import Feeds
from src.raindrop import Raindrop
import datetime as dt
import feedparser


def execute(args):
    logging.info("Loading subscription data.")
    feeds = Feeds("data/rainfeeds.opml")

    logging.info("Initialising Raindrop client.")
    try:
        raindrop_access_token = os.environ["RAINDROP_ACCESS_TOKEN"]
        raindrop = Raindrop(raindrop_access_token, "Inbox")
    except KeyError:
        logging.critical(
            "RAINDROP_ACCESS_TOKEN environment variable is not set.")
        sys.exit(1)

    datetime_fmt = "%a, %d %b %Y %H:%M:%S %Z"

    for feed in feeds:
        logging.info(f"Fetching {feeds[feed]["title"]}.")
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

        new_entries_count = len(new_entries)

        if len(new_entries) == 0:
            logging.info(f"No new {feeds[feed]["title"]} entries found.")
            continue

        logging.info(f"Sending {new_entries_count} entries to Raindrop.")
        responses = raindrop.create_raindrops(new_entries)

        for response in responses:
            if not response["result"]:
                logging.error(f"{response["errorMessage"]}")

        feeds[feed]["updated"] = now.strftime(datetime_fmt)
