import requests 
from bs4 import BeautifulSoup 
import csv
import re
import time
import pandas as pd


#urls = []

#for i in range(0,15):#
#	with requests.session() as s:
#		url = 'https://www.thecdg.co.uk/members/'
#		r = s.get(url)
#		soup = BeautifulSoup(r.content, 'lxml')
#		inputs = [i for i in soup.select(r'form input[type="hidden"]')]
#		form = {x['name']: x['value'] for x in inputs if x['value']} 
#		form['page'] = i + 1 
#		response = s.post('https://www.thecdg.co.uk/members/', data=form)
#	soup = BeautifulSoup(response.content, 'lxml')
#	links = [link.get('href') for link in soup.find_all(r'a') if re.search(r'https://www.thecdg.co.uk/members/', link.get('href'))]
#	urls.append(links)
#with open('urls.csv', 'w', encoding='utf-8') as csvfile:
#	writer = csv.writer(csvfile, delimiter=',')
#	[writer.writerow([i]) for i in urls]

#urls2 = []
#with open('urls.csv', newline='') as f:
#    reader = csv.reader(f)
#    for row in reader:
#        urls2.append([row])

#prelinks = [urls2[i][0][0] for i in range(0,len(urls2),2)]
#testlinks = []
#for o in prelinks:
#	o = o.split(',')
#	testlinks.append(o)



#actual = []
#for e in testlinks:
#	for i in e:
#		if i == "['https://www.thecdg.co.uk/members/'":
#			continue
#		elif i == 'https://www.thecdg.co.uk/members/':
#			continue
#		elif i.strip().strip(']').strip('[').strip("'") not in actual:
#			actual.append(i.strip().strip(']').strip('[').strip("'"))

prelist = []

#for i in range(len(actual)):
#	#source = requests.get(actual[i], time.sleep(2)).text
#	soup = BeautifulSoup(source,'lxml')
#	data = soup.find('table').text
#	dataII = data.split('\n\n')
#	dataIII = [i.split('\n') for i in dataII]
#	prelist.append(dataIII)

headers = {}

for i in prelist:
	for o in i:
		if '' in o:
			continue
		elif 'Nickname' in headers:
			track = len(headers['Nickname'])
			if o[0] in headers:
				if len(headers[o[0]]) == track:
					headers[o[0]].append(o[1])
				else:
					headers[o[0]].extend(['N/A' for i in range(track-1 - len(headers[o[0]]))])
					headers[o[0]].append(o[1])	
			else:
				headers[o[0]] = ['N/A' for i in range(track-1)]
				headers[o[0]].append(o[1])
		else:
			headers[o[0]] = [o[1]]
for i in headers:
	if i == 'Nickname':
		continue 
	elif len(headers['Nickname']) > len(headers[i]):
		headers[i].extend(['N/A' for i in range(len(headers['Nickname']) - len(headers[i]))])
	else:
		continue



df = pd.concat([pd.DataFrame(v, columns=[k]) for k, v in headers.items()], axis=1)
df.to_csv('testIV.csv')








#for i in actual:
#	source = requests.get(i, time.sleep(15)).text
#	print(source)
	#soup = BeautifulSoup(source,'lxml')
	#data.append(soup.find('table').find_all(text=True))








	









