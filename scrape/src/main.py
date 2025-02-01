from pathlib import Path
from bs4 import BeautifulSoup
import sys
import json

def main():
    songs=[]
    songs_json = open("./res/songs.json", mode="w")

    for file in Path("./res/ken").iterdir():
        with open(file, mode="r+") as file:
            html = BeautifulSoup(file, "html.parser")
            artist = html.select_one("h1").text
            items = html.select("section.trackItem")
            for item in items:
                name = item.select_one("span[itemprop=name]").text
                year = item.select_one("span.trackYear").text
                year = int(year.strip().replace("(", "").replace(")", ""))
                songs.append({ "artist": artist, "name": name, "year": year })

    json.dump(songs, songs_json, indent=4)
    return None

if __name__ == "__main__":
    main()
