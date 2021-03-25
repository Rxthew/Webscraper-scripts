import requests
from bs4 import BeautifulSoup
import csv
import re


# Takes a url from any cast and crew page on IMDB and -returns a raw dictionary
# with the names of the director/s and casting director/s.


def url_to_raw(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    keywords = re.compile(r"\bdirector\b|\bcasting_director\b", re.I)
    ID_tags = [i["id"] for i in soup.find_all(id=keywords)]
    Data = [
        soup.find("h4", attrs={"id": i}).find_next("tbody").find_all(text=True)
        for i in ID_tags
    ]
    raw_dict = {
        "Title": [soup.h3.find("a").text],
        "Director": Data[0],
        "Casting Director": Data[1],
    }
    return raw_dict


def raw_to_clean(
    raw_dict,
):  # takes the raw dictionary and cleans it of new line tags, whitespace, and empty strings.
    for i in raw_dict:
        if i == "Title":
            continue
        else:
            for o in raw_dict[i]:
                o = str(o)
                raw_dict[i][raw_dict[i].index(o)] = (
                    o.replace("\\n", "").replace("...", "credit:").strip()
                )
            raw_dict[i] = [i for i in filter(None, raw_dict[i])]
    clean = raw_dict
    return clean


def url_to_data(
    url,
):  # takes a url and returns the clean dictionary with the names of the director and casting director
    try:
        data = raw_to_clean(url_to_raw(url))
        name = data["Title"][0]
        with open(name + ".csv", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for i in data:
                writer.writerow([i])
                for o in data[i]:
                    writer.writerow([o])
        return
    except:
        return 'Failed to fetch data. Make sure you enter a url from IMDB where they feature "full credits and cast"'
