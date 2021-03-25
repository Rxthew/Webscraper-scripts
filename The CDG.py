import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def content_to_soup(page):
    return BeautifulSoup(page.content, "lxml")


"""
Following function gets links from specified page, no duplicate links

"""


def soup_to_links(soup):
    links = []
    [
        links.append(link.get("href"))
        for link in soup.find_all(r"a")
        if re.search(r"https://www.thecdg.co.uk/members/", link.get("href"))
        and link.get("href") not in links
    ]
    return links


"""
Following function which fills empty cells with 'N/A' (using the
length of the'Nickname' column as a baseline)

"""


def populate_null_fields(data):
    for label in data:
        if label == "Nickname":
            continue
        elif len(data["Nickname"]) > len(data[label]):
            data[label].extend(
                [
                    "N/A"
                    for i in range(len(data["Nickname"]) - len(data[label]))
                ]
            )
        else:
            continue
    return data


"""
	The following function takes list of lists, all lists have a length of 
	2, and converts them to a dictionary. The 1st entry in the lists are 
	the column labels of a table (e.g 'Nickname', 'telephone', 'e-mail').
	These are the dict's key. The 2nd entry is the actual info per person
	There is more than 1 person so the value for a given label is a list
	with separate info per item, per person. Whilst iterating, the 
	function checks if the column label is already in the dict, if Yes -
	adds to list. If Not - adds new key:value. The code also makes sure
	everything is aligned in case some column labels are present for 1
	person but not for another,(using the 'Nickname' column label as
	reference, since it is present for all.)

"""


def list_to_final(data):
    final = {}
    for lists in data:
        label, row_value = lists[0], lists[1]
        if "" in lists:  # skip empty strings
            continue

        elif "Nickname" in final:
            track = len(final["Nickname"])
            if label in final and len(final[label]) == track:
                final[label].append(row_value)
            elif label in final:
                final[label].extend(
                    ["N/A" for i in range(track - 1 - len(final[label]))]
                )
                final[label].append(row_value)
            else:
                final[label] = [row_value]

        else:
            final[label] = [row_value]
    return populate_null_fields(final)


# START of script

# Following gets urls of pages of casting directors from
# https://www.thecdg.co.uk/members and iterates through
# pages when posting form.

urls = []

for i in range(0, 15):
    with requests.session() as s:
        url = "https://www.thecdg.co.uk/members/"
        r = s.get(url)
        soup = content_to_soup(r)
        inputs = [i for i in soup.select(r'form input[type="hidden"]')]
        form = {x["name"]: x["value"] for x in inputs if x["value"]}
        form["page"] = i + 1
        response = s.post(url, data=form)
    urls += soup_to_links(content_to_soup(response))
    time.sleep(7)  # remembering to scrape politely

urls = (i for i in urls if i != "https://www.thecdg.co.uk/members/")

# Following goes to each casting director's webpage using urls just
# gathered. We get a table back for each, and after formatting,
# apply function abovementioned.

data_lists = []
for i in urls:
    source = requests.get(i, time.sleep(3))  # scrape politely.
    soup = content_to_soup(source)
    data_lists += soup.find("table").text.split("\n\n")
    data = (e.split("\n") for e in data_lists if e != "")

final = list_to_final(data)

# convert to csv file using pandas and download.

df = pd.concat(
    [pd.DataFrame(v, columns=[k]) for k, v in next(final).items()], axis=1
)
df.to_csv("casting_directors.csv")
print("File downloaded")

# END SCRIPT
