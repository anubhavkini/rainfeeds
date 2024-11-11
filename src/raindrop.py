import requests


class RaindropClient:
    def __init__(self, access_token: str):
        """
        Initialize Raindrop.io client

        Args:
            access_token (str): Raindrop.io API access token
        """
        self.base_url = "https://api.raindrop.io/rest/v1"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def get_user(self) -> dict:
        """
        Get user information from Raindrop.io

        Returns:
            Response from Raindrop.io API
        """
        response = requests.get(
            f"{self.base_url}/user",
            headers=self.headers
        )

        return response.json()

    def get_collection(self, id: int) -> dict:
        """
        Get collection information from Raindrop.io

        Args:
            id (int): ID of the collection

        Returns:
            Response from Raindrop.io API
        """
        response = requests.get(
            f"{self.base_url}/collection/{id}",
            headers=self.headers
        )

        return response.json()

    def create_raindrops(self, raindrops: list[dict]) -> dict:
        """
        Create raindrops in Raindrop.io

        Args:
            raindrops (List[Dict]): List of raindrops with key "url" and value "collection"

        Returns:
            Response from Raindrop.io API
        """
        payload = {
            "items": raindrops
        }

        response = requests.post(
            f"{self.base_url}/raindrops",
            headers=self.headers,
            json=payload
        )

        return response.json()


class Raindrop:
    def __init__(self, access_token: str, group: str):
        """
        Initialize Raindrop client

        Args:
            access_token (str): Raindrop.io API access token
            group (str, optional): Group name
        """
        self.client = RaindropClient(access_token)
        self.group = group
        self.collections = self._get_collections()

    def _get_group(self) -> dict:
        """
        Get group information from Raindrop.io

        Returns:
            Group information
        """
        groups = self.client.get_user()["user"]["groups"]

        for group in groups:
            if group["title"] == self.group:
                return group

    def _get_collections(self) -> dict:
        """
        Get collection information from Raindrop.io

        Returns:
            Collection information
        """
        group = self._get_group()

        collections = {}
        ids = group["collections"]

        for id in ids:
            collection = self.client.get_collection(id)
            collections[collection["item"]["title"]
                        ] = collection["item"]["_id"]

        collections["Unsorted"] = -1

        return collections

    def create_raindrops(self, raindrops: list[dict]) -> list[dict]:
        """
        Create raindrops in Raindrop.io

        Args:
            raindrops (List[Dict]): List of raindrops

        Returns:
            Responses from Raindrop.io API
        """
        raindrops_list = []
        response_list = []

        for raindrop in raindrops:
            raindrops_list.append({
                "pleaseParse": {},
                "created": raindrop["published"],
                "tags": [raindrop["publisher"]],
                "collection": {"$id": self.collections[raindrop["category"]]},
                "link": raindrop["link"]
            })

        batch_size = 100
        for i in range(0, len(raindrops_list), batch_size):
            response = self.client.create_raindrops(
                raindrops_list[i:i + batch_size])
            response_list.append(response)

        return response_list
