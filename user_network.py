from twitchcraft.reader import TwitchArchive
from collections import Counter

if __name__ == "__main__":
    ta = TwitchArchive("data/wapo.zip")

    ta.most_followed()
    