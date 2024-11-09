from src.feeds import Feeds
import feedparser
import json
from datetime import datetime


class FeedParser:
    @staticmethod
    def fetch_feed_entries(feed_url: str) -> list[dict]:
        """
        Fetch entries from a given feed URL

        Args:
            feed_url (str): URL of the RSS/Atom feed

        Returns:
            List of feed entries
        """
        feed = feedparser.parse(feed_url)
        return feed.entries


class FeedHistory:
    def __init__(self, history_file="data/history.json"):
        """
        Initialize feed history

        Args:
            history_file (str, optional): Path to the JSON file. Defaults to "data/history.json".
        """
        self.history_file = history_file
        self.history = self._load_history()

    def __del__(self):
        """
        Save history data to a JSON file
        """
        self._save_history()

    def _load_history(self) -> dict:
        """
        Load history data from a JSON file

        Returns:
            Dictionary containing last updated timestamp for each feed
        """
        try:
            f = open(self.history_file, 'r')
            return json.load(f)
        except:
            return {}

    def _save_history(self):
        """
        Save history data to a JSON file
        """
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def last_updated(self, feed_url: str) -> str:
        """
        Get the last updated timestamp for a given feed URL

        Args:
            feed_url (str): URL of the RSS/Atom feed

        Returns:
            Timestamp of the last updated feed
        """
        return self.history.get(feed_url)

    def update_last_updated(self, feed_url: str, last_updated: str):
        """
        Update the last updated timestamp for a given feed URL

        Args:
            feed_url (str): URL of the RSS/Atom feed
            last_updated (str): Timestamp of the last updated feed
        """
        self.history[feed_url] = last_updated


class FeedTracker:
    def __init__(self, feeds: Feeds, history_file="data/history.json"):
        """
        Initialize feed tracker

        Args:
            feeds (Feeds): Feeds object.
            history_file (str, optional): Path to the JSON file. Defaults to "data/history.json".
        """
        self.feeds = feeds
        self.history = FeedHistory(history_file)
        self.items = []

    def new_items(self) -> list[dict]:
        """
        Get new items from all feeds

        Returns:
            List of items
        """
        for feed in self.feeds:
            time_now = datetime.now()
            try:
                last_updated = datetime.fromtimestamp(
                    self.history.last_updated(feed))
            except TypeError:
                last_updated = None

            feed_entries = FeedParser.fetch_feed_entries(feed)
            for entry in feed_entries:
                entry_time = datetime(
                    entry["published_parsed"][0], entry["published_parsed"][1], entry["published_parsed"][2], entry["published_parsed"][3], entry["published_parsed"][4], entry["published_parsed"][5], entry["published_parsed"][6])
                if last_updated is None or entry_time > last_updated:
                    self.items.append({
                        "published": entry_time.isoformat(),
                        "publisher": self.feeds[feed]["title"],
                        "category": self.feeds[feed].get("category", "Unsorted"),
                        "link": entry["link"]
                    })

            self.history.update_last_updated(feed, time_now.timestamp())

        return self.items
