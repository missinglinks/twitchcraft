from zip_archive import ZipArchive
from collections import Counter
from tqdm import tqdm

class TwitchArchive:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.archive = ZipArchive(filepath)

        print("{} channels in archive".format(len(self.archive._archive.namelist())/3))



    def most_followed(self, n=50):
        follows = Counter()

        for filepath in tqdm(self.archive._archive.namelist()):
            if "follows" in filepath:
                data = self.archive[filepath]
                if "follows" in data:
                    follows.update([ x["channel"]["display_name"] for x in data["follows"] ])

        print(follows.most_common(n))

        