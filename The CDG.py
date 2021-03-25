import requests 
from bs4 import BeautifulSoup 
import re
import time
import pandas as pd


def content_to_soup(page): return BeautifulSoup(page.content, 'lxml')

def soup_to_links(soup):
	links = []
	[links.append(link.get('href')) for link in soup.find_all(r'a') if re.search(r'https://www.thecdg.co.uk/members/', link.get('href')) and link.get('href') not in links]
	return links

def populate_null_fields(data):
	for label in data:
		print(label)
		if label == 'Nickname':
			continue 
		elif len(data['Nickname']) > len(data[label]):
			data[label].extend(['N/A' for i in range(len(data['Nickname']) - len(data[label]))])
		else:
			continue
	return data

def list_to_final(data):
	final = {}
	for lists in data:
		label, row_value = lists[0], lists[1]
		if '' in lists:
			continue
		elif 'Nickname' in final:
			track = len(final['Nickname'])
			if label in final and len(final[label]) == track:
				final[label].append(row_value)
			elif label in final:
				final[label].extend(['N/A' for i in range(track-1 - len(final[label]))])
				final[label].append(row_value)
			else:
				final[label] = [row_value]
		else:
			final[label] = [row_value]
	return populate_null_fields(final) 

	
urls = []

for i in range(0,15): 
	with requests.session() as s:
		url = 'https://www.thecdg.co.uk/members/'
		r = s.get(url)
		soup = content_to_soup(r) 
		inputs = [i for i in soup.select(r'form input[type="hidden"]')] 
		form = {x['name']: x['value'] for x in inputs if x['value']} 
		form['page'] = i + 1 
		response = s.post(url, data=form)
	urls += soup_to_links(content_to_soup(response))
	time.sleep(8)

urls = (i for i in urls if i != 'https://www.thecdg.co.uk/members/')

data_lists = []
for i in urls:
		source = requests.get(i, time.sleep(8))
		soup = content_to_soup(source)
		data_lists += soup.find('table').text.split('\n\n')
		data = (e.split('\n') for e in data_lists if e != '')

final = list_to_final(data)


df = pd.concat([pd.DataFrame(v, columns=[k]) for k, v in next(final).items()], axis=1) 
df.to_csv('casting_directors.csv')










	









