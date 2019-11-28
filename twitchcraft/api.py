import requests

USER_URL = "https://api.twitch.tv/v5/users?login={username}&client_id={client_id}"
USER_FOLLOWS_URL = "https://api.twitch.tv/v5/users/{user_id}/follows/channels?client_id={client_id}"

CHANNEL_META_URL = "https://api.twitch.tv/v5/channels/{channel_id}/?client_id={client_id}"
CHANNEL_FOLLOWER_URL = "https://api.twitch.tv/v5/channels/{channel_id}/follows/?client_id={client_id}&limit=100&cursor={cursor}"
CHANNEL_VIDEOS_URL = "https://api.twitch.tv/v5/channels/462868995/videos/?client_id=s101slrbncp5fsjr4ze12t1a1y2gp1"

VIDEO_META_URL = "https://api.twitch.tv/v5/videos/{video_id}?client_id={client_id}"
VIDEO_COMMENTS_URL = "https://api.twitch.tv/v5/videos/{video_id}/comments?client_id={client_id}&cursor={cursor}"

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

    def __init__(self, client_id, verbose=False):
        self.verbose = verbose
        self.client_id = client_id

    def get_channel_id(self, username):
        rsp = self._call(USER_URL.format(
            username=username, 
            client_id=self.client_id))
        if rsp["_total"] == 1:
            channel_id = rsp["users"][0]["_id"]
            if self.verbose:
                print("Channel ID for username <{username}>: {channel_id}".format(
                    username=username, 
                    channel_id=channel_id))
            return rsp["users"][0]["_id"]
        elif rsp["_total"] == 0:
            if self.verbose:
                print("No channel found for username <{}>".format(username))
            return
        else:
            if self.verbose:
                print("Multiple channels found for username <{}>".format(username))
            return
    
    def get_channel_metadata(self, channel_id):
        rsp = self._call(CHANNEL_META_URL.format(
            channel_id=channel_id, 
            client_id=self.client_id))
        return rsp

    def get_followers(self, channel_id):
        cursor = ""
        follower = []

        while True:
            resp = self._call(CHANNEL_FOLLOWER_URL.format(
                channel_id=channel_id, 
                client_id=self.client_id, 
                cursor=cursor)) 

            follower += resp["follows"]

            if self.verbose:
                print("\r", end="")
                current_len = len(follower)
                print(current_len, end="")
            
            if "_cursor" in resp:
                cursor = resp["_cursor"]
            else:
                break  
        
        if self.verbose:
            print("\n Total followers: {}".format(len(follower)))
