import requests
from datetime import datetime

USER_URL = "https://api.twitch.tv/v5/users?login={username}&client_id={client_id}"
USER_FOLLOWS_URL = "https://api.twitch.tv/v5/users/{user_id}/follows/channels?client_id={client_id}&limit=100&offset={offset}"

CHANNEL_META_URL = "https://api.twitch.tv/v5/channels/{channel_id}/?client_id={client_id}"
CHANNEL_FOLLOWER_URL = "https://api.twitch.tv/v5/channels/{channel_id}/follows/?client_id={client_id}&limit=100&cursor={cursor}"
CHANNEL_VIDEOS_URL = "https://api.twitch.tv/v5/channels/462868995/videos/?client_id={client_id}"

VIDEO_META_URL = "https://api.twitch.tv/v5/videos/{video_id}?client_id={client_id}"
VIDEO_COMMENTS_URL = "https://api.twitch.tv/v5/videos/{video_id}/comments?client_id={client_id}&cursor={cursor}"

OFFSET_STEP = 100

class TwitchApi:
    """
    Wrapper class for the Twitch API. 
    Provides the following functionalities:
    * get channel id from username  
    * get channel metadata
    * [TODO] get all video ids from a channel
    * get all followers from a channel
    * [TODO] get video metadata
    * [TODO] get video chat messages
    """

    def _call(self, url):
        rsp = requests.get(url)
        return rsp.json()

    def __init__(self, client_id):
        self.client_id = client_id

    def get_channel_id(self, username, verbose=False):
        rsp = self._call(USER_URL.format(
            username=username, 
            client_id=self.client_id))
        if rsp["_total"] == 1:
            channel_id = rsp["users"][0]["_id"]
            if verbose:
                print("Channel ID for username <{username}>: {channel_id}".format(
                    username=username, 
                    channel_id=channel_id))
            return rsp["users"][0]["_id"]
        elif rsp["_total"] == 0:
            if verbose:
                print("No channel found for username <{}>".format(username))
            return
        else:
            if verbose:
                print("Multiple channels found for username <{}>".format(username))
            return
    
    def get_channel_metadata(self, channel_id):
        rsp = self._call(CHANNEL_META_URL.format(
            channel_id=channel_id, 
            client_id=self.client_id))

        metadata = {
            "retrieved_at": datetime.now().isoformat(),
            "meta": rsp
        }

        return metadata

    def get_followed_channels(self, user_id, verbose=False):
        offset = 0

        total = 0
        follows = []

        while True:
            rsp = self._call(USER_FOLLOWS_URL.format(
                user_id=user_id, 
                client_id=self.client_id,
                offset=offset))

            total = rsp["_total"]
            follows += rsp["follows"]

            if len(rsp["follows"]) == 0:
                break

            offset += OFFSET_STEP
        
        dataset = {
            "retrieved_at": datetime.now().isoformat(),
            "total": total,
            "follows": follows
        }
        print("\t\t Followed channels: {}".format(len(follows)))

        return dataset


    def get_follower(self, channel_id, verbose=False):
        cursor = ""
        follower = []

        while True:
            resp = self._call(CHANNEL_FOLLOWER_URL.format(
                channel_id=channel_id, 
                client_id=self.client_id, 
                cursor=cursor)) 

            follower += resp["follows"]

            if verbose:
                print("\r", end="")
                current_len = len(follower)
                print("\t\t{}".format(current_len), end="")
            
            if "_cursor" in resp:
                cursor = resp["_cursor"]
            else:
                break  
        
        if verbose:
            print("\n\t\tTotal followers: {}".format(len(follower)))
        
        dataset = {
            "retrieved_at": datetime.now().isoformat(),
            "follower": follower
        }

        return dataset
