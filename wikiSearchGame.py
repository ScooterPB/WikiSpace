#!/usr/bin/env python3

import requests
import urllib.request
from bs4 import BeautifulSoup
import webbrowser
from difflib import get_close_matches
import wikipedia
import re

countx=0

print("\n**Wiki Game**\n")

##Ask user to input title of starting page; verify that it is an active page & that it is the correct page they're looking for
while True:
	startLink = input("Please enter the title of the page to start searching from: ")
	##Verify that the starting term is correct
	try:
		st = wikipedia.page(startLink)
		stTerm = st.title
		yorn = input("Is '%s' the page you we should start the search from? (y/n)  " %stTerm)
		if yorn.lower() == 'y':
			try:
				sBD = stTerm.replace(" ","_")
				startURL = 'https://en.wikipedia.org/wiki/'+sBD
				break
			except:
				startURL = st.url
				break
		else:
			print("Please check the spelling of the page you are referencing and start again.\n")
	except wikipedia.exceptions.DisambiguationError as e:
		county = 0
		print("\nThe Title of the ending page you are looking for, '%s', couldn't be matched and returned the following results: " %startLink)
		for i in e.options:
			county += 1
			if county <= 9:
				print("[%s]   " %county,i)
			elif 10 <= county <= 99:
				print("[%s]  " %county,i)
			else:
				print("[%s] " %county,i)
		startInp = input("\nPlease specifcy which page you meant by typing the corresponding number: ")
		startTerm = str(e.options[int(startInp)-1])
		sttt = wikipedia.page(startTerm)
		startURL = sttt.url
		print("The wiki article we are starting on is: ",startTerm)
		break
	except:
		print("Couldn't locate the page you are referencing.")
		sCheck = input("Press 'x' to start search again OR enter the url of the correct page to start from: ")
		if sCheck == 'x':
			print()
		else:
			startURL = sCheck
			break

##Ask user to input title of page we are looking for; verify that it is an active page & that it is the correct page they're looking for
while True:		
	endLink = input("Please enter the title of the page you are looking for: ")
	##Verify the ending Title is correct
	try:
		ec = wikipedia.page(endLink)
		endTerm = ec.title
		eorn = input("Is '%s' the correct title that we are searching for? (y/n)  " %endTerm)
		if eorn.lower() == 'y':
			break
		else:
			print("Please re-enter the title of the article we are searching for.\n")
	except wikipedia.exceptions.DisambiguationError as e:
		count0 = 0
		print("\nThe Title of the ending page you are looking for, '%s', couldn't be matched and returned the following results: " %endLink)
		for i in e.options:
			count0 += 1
			if count0 <= 9:
				print("[%s]   " %count0,i)
			elif 10 <= count0 <= 99:
				print("[%s]  " %count0,i)
			else:
				print("[%s] " %count0,i)
		endInp = input("\nPlease specifcy which Title you meant by typing the corresponding number: ")
		endTerm = str(e.options[int(endInp)-1])
		print("The wiki article we are looking for is: ",endTerm)
		break
	except:
		try:
			ti = wikipedia.search(endLink)
			if ti != []:
				endTerm = ti[0]
				teorn = input("Is '%s' the correct title that we are searching for? (y/n)  " %endTerm)
				if teorn.lower() == 'y':
					break
				else:
					print("Please re-enter the title of the article we are searching for.\n")
		except:
			print("Failed to find a match for ending Title:",endlink)

##Ask the user to input any terms that they believe will help narrow down the search for the final page
helpLink = input("Please enter any keywords (seperated by commas) to associate with the title of the page you are looking for: ")
print("\nVerifying Search Terms...")
if helpLink != '':
	hLin2 = helpLink.split(', ')
else:
	hLin2 = []
hLinList = []
for i in hLin2:
	try:
		t = wikipedia.page(i)
		g = t.title
		hLinList.append(g)
	except wikipedia.exceptions.DisambiguationError as e:
		count = 0
		print("\nThe search term '%s' returned the following results: " %i)
		for i in e.options:
			count += 1
			if count <= 9:
				print("[%s]   " %count,i)
			elif 10 <= count <= 99:
				print("[%s]  " %count,i)
			else:
				print("[%s] " %count,i)
		userInp = input("\nPlease specifcy which search term you meant by typing the corresponding number: ")
		hLinList.append(e.options[int(userInp)-1])
	except:
		try:
			t = wikipedia.search(i)
			if t != []:
				hLinList.append(t[0])
		except:
			print("Failed to find a match for search term:",i)
print("Searching...\n")
					
x = endTerm
y = hLinList
history = []

##Wiki Search Game Function (NOTE: 'circuitB' is useless rn... placeholder for future features)
def scrape(url, end, helps, circuitB):
	global countx
	global x
	global y
	response = requests.get(url)

	##Scraping of links from webpage passed through the 'url' variable
	soup = BeautifulSoup(response.text, features='html.parser')

	linklist = soup.findAll('a')[0:]
	dict = {}
	searchKey = 'origin'
	p1 = []
	p2 = []
	p3 = []
	p4 = []
	helper = list(filter(('').__ne__,helps))
	h0List = []
	h1List = []
	h2List = []
	h3List = []
	enders = end.split()
	e1List = []
	e2List = []


	##Prioritize the scraped links based off of their relation to 'EndGoal'
	for i in linklist:
		if 'href' in str(i) and i.get('title') != None:
			dict.update({i.get('title'):i['href']})
			pattern = '>(.*?)</a>'
			try:
				substring = re.search(pattern, str(i)).group(1)
			except:
				substring = ''
			if str(end) == str(i.get('title')):
				priority1 = i.get('title')
				p1.append(priority1)
			elif str(end) in str(i.get('title')):
				priority2 = i.get('title')
				p2.append(priority2)
			elif str(end) in str(substring):
				priority3 = i.get('title')
				p3.append(priority3)
			elif str(end) in str(i):
				priority4 = i.get('title')
				p4.append(priority4)
			for e in helper:
				if e == str(i.get('title')):
					h0List.append(i.get('title'))
				elif e in str(i.get('title')):
					h1List.append(i.get('title'))
				elif e in str(substring):
					h2List.append(i.get('title'))
				elif e in str(i):
					h3List.append(i.get('title'))
			for p in enders:
				if p in str(i.get('title')):
					e1List.append(i.get('title'))
				elif p in str(substring):
					e2List.append(i.get('title'))
				
	if p1 != []:
		while True:
			for i in p1:
				if i not in history:
					searchKey = i
					break
			break
	elif p2 != []:
		while True:
			for i in p2:
				if i not in history:
					searchKey = i
					break
			break
	elif p3 != []:
		while True:
			for i in p3:
				if i not in history:
					searchKey = i
					break
			break
	elif p4 != []:
		while True:
			for i in p4:
				if i not in history:
					searchKey = i
					break
			break


	##Search the links to determine if any of them prove to be similar to 'EndGoal' & 'Helping Key Words'	
	#Searching for Helping Words in Links
	helpResults = []
	for i in helper:
		helpMatch = get_close_matches(i, dict.keys(), 1, cutoff=0.75)
		if helpMatch != []:
			helpResults.append(helpMatch[0])
		
	urlNew = 'origin'
	hList = []
	helpList = []
	keyWordList = []
	for i in helpResults:
		if i in history:
			history
		elif str(i) in helper:
			hList.append(str(i))
		else:
			helpList.append(i)
	if h0List != []:
		keyWordList.extend(h0List)
	if h1List != []:
		keyWordList.extend(h1List)
	if h2List != []:
		keyWordList.extend(h2List)
	if h3List != []:
		keyWordList.extend(h3List)
	if hList != []:
		keyWordList.extend(hList)
	if helpList != []:
		keyWordList.extend(helpList)
		
	#Will leverage this list only if unable to find 'prioritized links' or 'helping key word links'
	searchResults = get_close_matches(end, dict.keys(), 10, cutoff=0.2)

	#If we found 'keywords' in links, decide which link to search through next (based off search history)
	if searchResults[0] != end and keyWordList != [] and searchKey == 'origin':
		while True:
			for i in keyWordList:
				if i not in history:
					searchKey = i
					break
				else:
					print("Keyword already searched.")
					#Potentially add Dict feature here
			break
		
	#Remove keyWord from Search Keys if we visited the wiki page for that KeyWord (restart with all keywords if we hit 'random article')
	for i in helper:
		if i == searchKey:
			helper.remove(i)
	helped = helper
		
	#If no new link is determined yet, we will look if any links are similar to any of the individual words in 'EndGoal' if applicable
	#If still no link is found, we will search for links with titles similar to 'EndGoal' (i.e. using 'get_close_matches)
	#If no valid links are found, we will pull a random link		
	if searchKey == 'origin':
		step3check = 0
		if e1List != []:
			for i in e1List:
				if i not in history:
					searchKey = i
					print("Search term: ",searchKey)
					step3check = 1
					break
		if e2List != [] and step3check == 0:
			for i in e2List:
				if i not in history:
					searchKey = i
					print("Search term: ",searchKey)
					step3check = 1
					break
		if step3check == 0:
			historyCheck = 0
			while True:
				for i in searchResults:
					if i not in history:
						historyCheck = i
						print("Search term: ", i)
						break
				if  historyCheck == 0:
					print("Search Term Dead End.\n")
					urlNew = 'https://en.wikipedia.org/wiki/Special:random'
					break
				else:
					searchKey = historyCheck
					break
	else:
		print("Search term: ",searchKey)	


	##Compare the new search term (link) against the 'EndGoal' & check to ensure webpage is real
	if searchKey == end:
		countx = countx + 1
		history.append(searchKey)
		print("\nSuccess! It took", countx, "searches to reach '"+end+"'.\n")
		print("Searches: ")
		for i in history:
			if i in y:
				print(i+'*')
			else:
				print(i)
		print("\n* Denotes a 'Keyword' search term\n")
		webbrowser.open('https://en.wikipedia.org'+dict[searchKey])
	elif urlNew == 'https://en.wikipedia.org/wiki/Special:random':
		history.append("<Reset with Random Article>")
		scrape(urlNew, x, y, 0)
	else:
		countx = countx + 1	
		history.append(searchKey)
		liveURL = wikipedia.search(searchKey)
		if liveURL == []:
			print("Dead End.")
			urlNew = 'https://en.wikipedia.org/wiki/Special:random'
			history.append("<Reset with Random Article>")
			scrape(urlNew, x, y, 0)
		else:
			try:
				searchURL = wikipedia.page(liveURL[0])
				urlNew = searchURL.url
				scrape(urlNew, x, helped, 0)
			except wikipedia.exceptions.DisambiguationError as e:
				for i in e.options:
					try:
						newVari = i
						searchURL = wikipedia.page(newVari)
						urlNew = searchURL.url
						history.append(newVari)
						countx = countx + 1
						print("Search Term: ",newVari)
						scrape(urlNew, x, helped, 0)
						break
					except:
						print("Error with Options.")
						urlNew = 'https://en.wikipedia.org/wiki/Special:random'
						history.append("<Reset with Random Article>")
						scrape(urlNew, x, y, 0)
						break
			except wikipedia.exceptions.PageError:
				try:
					urlPlug = re.sub("\s+", "_", searchKey.strip())
					urlNew = 'https://en.wikipedia.org/wiki/'+urlPlug
					scrape(urlNew, x, helped, 0)
				except:
					print("Broken Page.")
					urlNew = 'https://en.wikipedia.org/wiki/Special:random'
					history.append("<Reset with Random Article>")
					scrape(urlNew, x, y, 0)
			except:
				print("Broken Link.")
				urlNew = 'https://en.wikipedia.org/wiki/Special:random'
				history.append("<Reset with Random Article>")
				scrape(urlNew, x, y, 0)


scrape(startURL, endTerm, hLinList, 0)