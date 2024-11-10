# Rainfeeds
**Rainfeeds** watches your RSS and Atom feeds and pushes new items to your [Raindrop](https://raindrop.io).
## Setup
Clone this repository and run
```shell
pip install .
```
Create a Raindrop API [Test token](https://developer.raindrop.io/v1/authentication/token) and define it in the environment
```shell
export RAINDROP_ACCESS_TOKEN=<your-test-token>
```
## Usage
```shell
# list feeds
rainfeeds ls

# add a feed
rainfeeds add [-t TITLE] [-c CATEGORY] url

# remove a feed
rainfeeds rm url

# edit a feed
rainfeeds edit [-h] [-t TITLE] [-c CATEGORY] url

# send new feed entries to raindrop
rainfeeds sync
```
## Running sync in a container
Create the container
```shell
podman container create \
--name rainfeeds \
-v $PATH_TO_DATA_DIR:/app/data \
-e RAINDROP_ACCESS_TOKEN \
ghcr.io/anubhavkini/rainfeeds:main
```
Send new feed entries to raindrop
```shell
podman start -ai rainfeeds
```
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.