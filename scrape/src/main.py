from pathlib import Path
from bs4 import BeautifulSoup
import sys
import json
from time import sleep
from playwright.sync_api import sync_playwright
import itertools

id_counter = 100

def main():
    global id_counter 

    # sampled = {
    #     "id": 0,
    #     "name": "Good Times",
    #     "year": 1979,
    #     "artist": "Chic"
    # }
    # playwright("https://www.whosampled.com/Chic/Good-Times/sampled/", sampled)
    # sampled = {
    #     "id": 0,
    #     "name": "Everybody Loves the Sunshine",
    #     "year": 1976,
    #     "artist": "Roy Ayers Ubiquity"
    # }
    # playwright("https://www.whosampled.com/Roy-Ayers-Ubiquity/Everybody-Loves-the-Sunshine/sampled/", sampled)
    # sampled = {
    #     "id": 0,
    #     "name": "C.R.E.A.M.",
    #     "artist": "Wu-Tang Clan",
    #     "year": 1993,
    # }
    # playwright("https://www.whosampled.com/Wu-Tang-Clan/C.R.E.A.M./sampled/", sampled)
    sampled = {
        "id": 100,
        "name": "Shook Ones Part II",
        "artist": "Mobb Deep",
        "year": 1994,
    }
    playwright("https://www.whosampled.com/Mobb-Deep/Shook-Ones-Part-II/sampled/", sampled)
    sys.exit(0)

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

                sampled = []
                for con in item.select("div.track-connection"):
                    label = con.select_one("span.sampleAction").text.strip()
                    if label == "sampled":
                        find_and_parse_ul(con, sampled)
                    if label == "was sampled in":
                        find_and_parse_ul(con, songs)

                songs.append({
                    "id": id_counter,
                    "artist": artist,
                    "name": name,
                    "year": year,
                    "sampled": sampled
                })
                id_counter += 1

    json.dump(songs, songs_json, indent=2)

def find_and_parse_ul(node, array):
    global id_counter 

    ul = node.select_one("ul")
    for li in ul.select("li"):
        a = li.select("a")
        name = a[0].text.strip()
        artist = ""
        try:
            artist = a[1].text.strip()
        except IndexError:
            artist = li.select_one("strong").text.strip()

        li = li.text.strip()
        year = li[li.rfind("(")+1:len(li)-1]

        array.append({
            "id": id_counter,
            "artist": artist,
            "name": name,
            "year": year,
            "sampled": []
        })
        id_counter += 1

def playwright(link, sampled):
    # with open("log.txt", mode="a+") as log:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=2000)
        crawl_songs_that_sampled(browser, link, sampled)
        browser.close()
        print(id_counter)

def crawl_songs_that_sampled(browser, link, sampled):
    global id_counter

    with open("log.txt", mode="a+") as log:
        for idx in itertools.count(start=1):
            page = browser.new_page()
            linkIdx=f"{link}?cp={idx}"
            print(linkIdx)
            page.goto(linkIdx)
            html = BeautifulSoup(page.content(), "html.parser")

            if "Page Not Found" in html.h1.text:
                sleep(1)
                page.close()
                return

            try:
                trs = html.table.tbody.find_all("tr")
            except:
                print("Error:")
                continue

            for tr in trs:
                info = tr.find_all("td")
                nameA = info[1].a
                href = nameA.get("href")
                name = nameA.text.strip()
                artist = info[2].a.text.strip()
                year = info[3].text.strip()
                current = {
                    "id": id_counter,
                    "artist": artist,
                    "name": name,
                    "year": int(year),
                    "sampled": [sampled]
                }
                # /sample/7063/Dr.-Dre-My-Life-Roy-Ayers-Ubiquity-Everybody-Loves-the-Sunshine/
                after_c_artist = find_nth(href, "/", 3) + len(artist) + 1
                sampled_artist = sampled["artist"].replace(" ", "-")
                before_s_artist = href.find(sampled_artist)
                newLink=href[find_nth(href, "/", 3)+1:before_s_artist-1]
                newLink=replace(newLink, len(artist), "/")
                
                log.write(f"{json.dumps(current)}\n")
                print(id_counter)
                id_counter += 1
                crawl_songs_that_sampled(browser, \
                                         f"https://www.whosampled.com/{newLink}/sampled/", \
                                         current)

        sleep(1)
        page.close()


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def replace(s, position, character):
    return s[:position] + character + s[position+1:]

    # for idx in itertools.count(start=1):
    #     page = browser.new_page()
    #     page.goto(f"{link}?cp={idx}")
    #     # if "Just in waiting..." in page.title():
    #     #     input("Press ENTER to continue")
    #     page = BeautifulSoup(page.content(), "html.parser")
    #
    #     sleep(2)


if __name__ == "__main__":
    main()
