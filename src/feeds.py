import xml.etree.ElementTree as ET
import feedparser


class Feeds:
    def __init__(self, feeds_file_path: str):
        self._feeds_file_path = feeds_file_path
        self._feeds = {}
        self._load(self._feeds_file_path)

    def __del__(self):
        self._save(self._feeds_file_path)

    def __iter__(self):
        return iter(self._feeds)

    def __getitem__(self, key):
        return self._feeds[key]

    def __setitem__(self, key, value):
        self._feeds[key] = value

    def __delitem__(self, key):
        del self._feeds[key]

    def __contains__(self, key):
        return key in self._feeds

    def _load(self, feeds_file_path: str) -> dict:
        """
        Parse an OPML file and extract feed information

        Args:
            feeds_file_path (str): Path to the OPML file
        """
        tree = ET.parse(feeds_file_path)
        root = tree.getroot()

        # Find all outline elements with xmlUrl attribute
        for outline in root.findall(".//outline[@xmlUrl]"):
            title = outline.get("text")
            category = outline.get("category")
            url = outline.get("xmlUrl")

            self[url] = {"title": title}
            if category is not None:
                self[url]["category"] = category

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

        for url in self:
            outline = ET.SubElement(
                body, "outline", text=self[url]["title"], type="rss", xmlUrl=url)
            if "category" in self[url]:
                outline.set("category", self[url]["category"])

        tree = ET.ElementTree(root)
        tree.write(feeds_file_path, encoding="utf-8", xml_declaration=True)

    def list(self):
        """
        Print out a list of feeds, in the format:

        <title> [<category>]
          <url>
        """
        for url in self:
            print(f"{self[url]["title"]} [{
                  self[url]["category"]}]\n  {url}\n")

    def add(self, url: str, title: str = None, category: str = None):
        """
        Add a new feed to the list

        Args:
            url (str): URL of the RSS/Atom feed
            title (str, optional): Title of the feed. Defaults to None.
            category (str, optional): Category of the feed. Defaults to None.
        """
        if url in self:
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
            self[url] = {"title": title, "category": category}
        else:
            self[url] = {"title": title}

    def remove(self, url: str):
        """
        Remove a feed from the list

        Args:
            url (str): URL of the RSS/Atom feed
        """
        try:
            del self[url]
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
        if url not in self:
            print("Feed does not exist.")
            return

        if title is not None:
            self[url]["title"] = title
        if category is not None:
            if category == '':
                del self[url]["category"]
            else:
                self[url]["category"] = category
