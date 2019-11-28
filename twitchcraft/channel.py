import os
import sys
from .api import TwitchApi
from zip_archive import ZipArchive

DATA_DIR = "data"

class ChannelDownloader:
    """
    Downloads twitch channel metadata and stores it into a zip archive
    """

    def _metadata_file(self, username):
        return "{username}/metadata.json".format(username=username)

    def _follower_file(self, username):
        return "{username}/follower.json".format(username=username)
    
    def _follows_file(self, username):
        return "{username}/follows.json".format(username=username)

    def __init__(self, client_id, project, overwrite=False):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)

        self.archive_file = os.path.join(DATA_DIR, "{}.zip".format(project))
        self.archive = ZipArchive(self.archive_file, overwrite=overwrite)

        self.api = TwitchApi(client_id)

    def _fetch_by_channel_id(self, channel_id, username):
        if not channel_id:
            print("No channel found for username!")
            sys.exit(1)

        metadata_file = self._metadata_file(username)
        if not metadata_file in self.archive:        
            print("\t fetching channel metadata ...")
            meta = self.api.get_channel_metadata(channel_id)
            self.archive[metadata_file] = meta

        follower_file = self._follower_file(username)
        if not follower_file in self.archive:
            print("\t fetching channel followers ...")
            follower = self.api.get_follower(channel_id, verbose=True)
            self.archive[follower_file] = follower

        follows_file = self._follows_file(username)
        if not follows_file in self.archive:
            print("\t fetching followed channels ...") 
            follows = self.api.get_followed_channels(channel_id)
            self.archive[follows_file] = follows


    def fetch(self, username):
        channel_id = self.api.get_channel_id(username)
        self._fetch_by_channel_id(channel_id, username)

    
    def fetch_channel_followers(self, username):
        follower_file = self._follower_file(username)
        if not follower_file in self.archive:
            print("fetch <{}>".format(username))
            self.fetch(username)

        follower = self.archive[follower_file]["follower"]
        follower_count = len(follower)

        for i, f in enumerate(follower):
            print("[{}/{}] fetch <{}>".format(i, follower_count, f["user"]["name"]))
            self._fetch_by_channel_id(f["user"]["_id"], f["user"]["name"])
