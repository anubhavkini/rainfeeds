import xml.etree.ElementTree as ET
import feedparser


class Feeds:
    def __init__(self, feeds_file_path: str):
        self.feeds_file_path = feeds_file_path
        self.feeds = self._load(self.feeds_file_path)

    def __del__(self):
        self._save(self.feeds_file_path)

    def _load(self, feeds_file_path: str) -> dict:
        """
        Parse an OPML file and extract feed information

        Args:
            feeds_file_path (str): Path to the OPML file

        Returns:
            List of dictionaries containing feed information
        """
        feeds = {}

        tree = ET.parse(feeds_file_path)
        root = tree.getroot()

        # Find all outline elements with xmlUrl attribute
        for outline in root.findall(".//outline[@xmlUrl]"):
            title = outline.get("text")
            category = outline.get("category")
            url = outline.get("xmlUrl")

            feeds[url] = {"title": title}
            if category is not None:
                feeds[url]["category"] = category

        return feeds

    def _save(self, feeds_file_path: str):
        """
        Save feeds to an OPML file

        Args:
            feeds_file_path (str): Path to the OPML file
        """
        root = ET.Element("opml", version="2.0")

        head = ET.SubElement(root, "head")
        title = ET.SubElement(head, "title")
        title.text = "Rainfeeds"

        body = ET.SubElement(root, "body")

        for url in self.feeds:
            outline = ET.SubElement(
                body, "outline", text=self.feeds[url]["title"], type="rss", xmlUrl=url)
            if "category" in self.feeds[url]:
                outline.set("category", self.feeds[url]["category"])

        tree = ET.ElementTree(root)
        tree.write(feeds_file_path, encoding="utf-8", xml_declaration=True)

    def list(self):
        """
        Print out a list of feeds, in the format:

        <title> [<category>]
          <url>
        """
        for url in self.feeds:
            print(f"{self.feeds[url]["title"]} [{
                  self.feeds[url]["category"]}]\n  {url}\n")

    def add(self, url: str, title: str = None, category: str = None):
        """
        Add a new feed to the list

        Args:
            url (str): URL of the RSS/Atom feed
            title (str, optional): Title of the feed. Defaults to None.
            category (str, optional): Category of the feed. Defaults to None.
        """
        if url in self.feeds:
            print("Feed already exists.")
            return

        feed = feedparser.parse(url)

        if feed.version == '':
            print("Invalid feed.")
            return

        if title is None:
            try:
                title = feed["feed"]["title"]
            except KeyError:
                title = "Untitled Feed"

        if category is not None:
            self.feeds[url] = {"title": title, "category": category}
        else:
            self.feeds[url] = {"title": title}

    def remove(self, url: str):
        """
        Remove a feed from the list

        Args:
            url (str): URL of the RSS/Atom feed
        """
        try:
            del self.feeds[url]
        except KeyError:
            print("Feed does not exist.")

    def edit(self, url: str, title: str = None, category: str = None):
        """
        Edit a feed in the list

        Args:
            url (str): URL of the RSS/Atom feed
            title (str, optional): New title of the feed. Defaults to None.
            category (str, optional): New category of the feed. Defaults to None.
        """
        if url not in self.feeds:
            print("Feed does not exist.")
            return

        if title is not None:
            self.feeds[url]["title"] = title
        if category is not None:
            if category == '':
                del self.feeds[url]["category"]
            else:
                self.feeds[url]["category"] = category
