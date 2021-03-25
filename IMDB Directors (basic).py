import requests 
from bs4 import BeautifulSoup 
import csv
import re

#Takes a url from any cast and crew page on IMDB and -returns a raw dictionary
#with the names of the director/s and casting director/s.

def url_to_raw(url):  
		source = requests.get(url).text        
		soup = BeautifulSoup(source,'lxml') 
		keywords = re.compile(r'\bdirector\b|\bcasting_director\b', re.I)
		ID_tags = [i['id'] for i in soup.find_all(id=keywords)]
		Data = [soup.find('h4', attrs={'id':i})\
		   .find_next('tbody').find_all(text=True)for i in ID_tags]
		raw_dict = {'Title': [soup.h3.find('a').text], 'Director': Data[0],'Casting Director': Data[1]}
		return raw_dict

def raw_to_clean(raw_dict): #takes the raw dictionary and cleans it of new line tags, whitespace, and empty strings.     
	for i in raw_dict: 
		if i == 'Title':
			continue
		else:
			for o in raw_dict[i]:
				o = str(o)
				raw_dict[i][raw_dict[i].index(o)]\
				= o.replace("\\n", "").replace("...","credit:").strip()
			raw_dict[i]= [i for i in\
			filter(None, raw_dict[i])]
	clean = raw_dict
	return clean
		

def url_to_data(url): #takes a url and returns the clean dictionary with the names of the director and casting director
	try:
		data = raw_to_clean(url_to_raw(url))
		name = data['Title'][0]
		with open(name + '.csv', 'w', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for i in data: 
				writer.writerow([i])
				for o in data[i]:
					writer.writerow([o])
		return 
	except:
		return 'Failed to fetch data. Make sure you enter a url from IMDB where they feature "full credits and cast"'

#ATTENTION: NEED TO HANDLE NOTIFICATION TO USER PART WHERE A BUNCH OF 'NO RESULTS FOUND' GET PRINTED TO THE NOTEPAD THING. 





#The following is some roughwork and rejected procedures I used leading up to the final script. 

#Takes a url from any cast and crew page on IMDB and -returns a raw dictionary
#with the names of the director/s and casting director/s.

#def url_to_raw(url):  
#	source = requests.get(url).text        
#	soup = BeautifulSoup(source,'lxml') 
#	keywords = re.compile(r'\bdirector\b|\bcasting_director\b', re.I)
#	ID_tags = soup.find_all(id=keywords)
#	title = soup.h3.find('a').text
#	raw_dict =  [title, {i['id']: soup.find('h4', attrs={'id':i['id']})\
#	.find_next('tbody').find_all(text=True)for i in ID_tags}]
#	return raw_dict

#def raw_to_clean(raw_dict): #takes the raw dictionary and cleans it of new line tags, whitespace, and empty strings. 
#	for i in raw_dict[1]:
#		for o in raw_dict[1][i]:
#			o = str(o)
#			raw_dict[1][i][raw_dict[1][i].index(o)]\
#		 	= o.replace("\\n", "").replace("...","credit:").strip()
#		raw_dict[1][i]= [i for i in\
#		filter(None, raw_dict[1][i])]
#	clean = raw_dict
#	if clean[1] == {}:
#		clean = 'No results found. Are you sure you have entered a url from IMDB where they feature "full credits and cast"?'
#	return clean

#def url_to_soup(url):
#	source = requests.get(url).text
#	soup = BeautifulSoup(source,'lxml')
#	return soup

#def soup_to_IDs(soup):
#	keywords = re.compile(r'^director$|^casting_director$', re.I)
#	ID_tags = soup.find_all(id=keywords)
#	list_of_ids = []
#	[list_of_ids.append(i['id']) for i in ID_tags]
#	return list_of_ids

#def IDs_to_data(soup, list_of_ids):
#	tables = {}
#	for i in list_of_ids:
#		for tag in soup.find_all(True):
#			if tag.has_attr('id') and tag['id']==i:
#				tables[i]=[tag.next_sibling.next_sibling.tbody]
#	data = []
#	for i in tables:

#		[data.append({i[0]:tr}) for tr in  i[1].find_all(True, recursive=False)]
#	return data[0]['director']

#def url_to_data(url):
#	soup = url_to_soup(url)
#	list_of_ids = soup_to_IDs(soup)
#	return IDs_to_data(soup, list_of_ids)
#print(url_to_data('https://www.imdb.com/title/tt0944947/fullcredits?ref_=tt_ql_1'))


#for e in range(0,1):
#	print(str(stuff[e]).replace(" ",'').replace("\\n", '').replace("''","").replace(',',''))

#for e in range(0,1):
#	print(str(stuff[e]).strip("\\n"))

#for e in range(0,1):
#	print(str(stuff[e]).replace("\\n", ""))

#for e in range(0,1):
#	print(str(stuff[e]))

#for e in range(0,1):
#	print(str(stuff[e]).strip("\\n"))


#for e in range(0,1):
#	for i in stuff[e]:
#		print(i.strip(''))


#stuff = [[[e('a')],[e('td', attrs={'class':['credit']})]] for e in [i.next_sibling.next_sibling.tbody for i in ID_tags]]


#print(soup_to_IDs(url_to_soup('https://www.imdb.com/title/tt0944947/fullcredits?ref_=tt_ql_1')))

#if tag.next_sibling.has_attr('class'):
#					new_tag = tag.next_sibling.has_attr('class') 
#					data.append({i:{new_tag['class']=='name': new_tag['class']=='credit'}.text})


#def url_to_tags(url):
#	source = requests.get(url).text
#	soup = BeautifulSoup(source,'lxml')
#	keywords = re.compile('director|casting', re.I)
#	ID_tags = soup.find_all(id=keywords)
#	return ID_tags

#def Get_IDs(list):
#	IDs = []
#	[IDs.append(i['id']) for i in list]
#	return IDs

#def Get_All_Names(ID_list):
#	for i in ID_list:#
#		for tag in soup.find_all(True):
#			if tag.has_attr('id') and i in tag['id']:
#				return (tag.find_next('tbody').text)

#def IDs_to_list(tags):
#	ID_list = Get_IDs(tags)
#	Data = Get_All_Names(ID_list)
#	return Data

#def url_to_data(url):
#	tags = url_to_tags(url)
#	return IDs_to_list(tags)


#for i in IDs: THIS WORKS
#	for tag in soup.find_all(True):
#		if tag.has_attr('id') and i in tag['id']:
#			print (tag.find_next('tbody').text)	


#url = 'https://www.imdb.com/title/tt0944947/fullcredits?ref_=tt_ql_1'
#source = requests.get(url).text
#soup = BeautifulSoup(source, 'lxml')
#keywords = re.compile('director|casting', re.I)
#ID_locations = soup.find_all(id=keywords)#

#IDs = something(ID_locations)


#for i in soup.find_all('h4'):
#	print(i.get('id'))

#b = soup.find('h4')
#print(b.find_parent(True))


#for i in h4_List:
#	print (soup(i).find_next('tbody').text)


#print (soup.find_all('h4').find_next('tbody').text)


#print(soup.find_all(id=keywords))
#marks = [i for i in soup.find_all(id=keywords)]
#[print(soup.h4.find_next('tbody').text) for i in marks if i in soup.find_all('h4')]
#donkey = [soup.h4.find_next('tbody').text for h4 in soup.find_all('h4') if 'director' or 'casting' in h4['id']]


#print(soup.h4.find_next('tbody').text)




  
