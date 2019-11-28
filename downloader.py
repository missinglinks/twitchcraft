from twitchcraft.channel import ChannelDownloader
from config import CLIENT_ID, PROJECT

if __name__ == "__main__":

    cdl = ChannelDownloader(client_id=CLIENT_ID, project=PROJECT)
    #cdl.fetch("lostmojo27")
    cdl.fetch_channel_followers("donaldtrump")