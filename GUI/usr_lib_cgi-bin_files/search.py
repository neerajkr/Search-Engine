#!/usr/bin/python
import cgi, cgitb
import urllib2 
import sqlite3
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import lxml.html
import requests
import codecs
import re
from time import time
start_time=time()
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict


start_time=time()
########## function to insert quotes in a string ##################
def quotes(s1):
    return "'%s'" % s1



################# Search keywords ###############################
form = cgi.FieldStorage() 
SearchPhrase = form.getvalue('search')
tokenizer = RegexpTokenizer(r'\w+')
SearchWords=tokenizer.tokenize(SearchPhrase)


############### Sqlite Database handling ##################
con=sqlite3.connect('SearchEngineDB_new.db')
c=con.cursor()
file_cur=con.cursor()

################# HTML presentation #######################
print "Content-type:text/html\r\n\r\n"
print """<html>
 		<head>
		<title>Search Engine</title>
		<link rel="stylesheet" href="css/style.css">

 		</head>	
		<body>
		<form class="searchbox" action="/cgi-bin/search.py">
        <input type="search"  name="search" placeholder="search.." />       
    </form>
		"""

# print "<h2>SearchWords: %s</h2>"%(SearchWords)

################### Forming SearchQuery ##################

SearchQuery="KEYWORD like "
count=1
for word in SearchWords:
	# print "<h2>word: %s</h2>"%(word)
	if count==1:
		SearchQuery=SearchQuery+quotes(word)
	else:
		SearchQuery=SearchQuery+" OR KEYWORD like "+ quotes(word)
	count=count+1
SearchQuery="SELECT URL, SUM(TOTAL_WEIGHT) as TOTAL_WEIGHT from KEYWORD_RANK where "+SearchQuery+" GROUP BY URL order by TOTAL_WEIGHT Desc"
c.execute(SearchQuery)
results=c.fetchall()

# print "<h5>SearchQuery: %s</h5>"%(SearchQuery)
print "<h5>Number Of results: %s (%s seconds)</h5> "% (len(results),time()-start_time)



###################### Displaying Search Results ##################
i=0
for URL,WEIGHT in results:

	# print "<h6>url: %s</h6>"%(URL)
	# print "<h6>weight: %s</h6>"%(WEIGHT)	

	i=i+1

	if i==10:
		break
	# print "<h4>Result: %s</h4>"%(i)
	file_cur.execute('SELECT FILE_LOCATION FROM KEYWORD_RANK WHERE URL=?',(URL,))
	file_location=file_cur.fetchone()[0]
	
	file_location=file_location.split('/')
	site_id=file_location[1]
	url_id=file_location[2]

	FilePath="/home/linux/Desktop/TotorialsPoint/dec27/"+site_id+"/"+url_id
	html = urllib.urlopen(FilePath).read()    #HTML content
	soup = BeautifulSoup(html,"lxml")



	############## Title of Page ##################
	PageTitle=soup.title.string
	if PageTitle:
		PageTitle=PageTitle
	else:
		PageTitle=""			
	

	# # ################# MetaDes Extraction #########################

	# descKey=soup.findAll(attrs={"name":"Description"})
	# if descKey:
	# 	descKey=descKey[0]['content'].encode('utf-8')
	# else:
	# 	descKey=""
	# MetaDes=descKey

	################## Pre-Processing Of Text ###############################

	# data = soup.findAll(text=True)
	# [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	# visible_text = soup.getText()

	
	
	
		# kill all script and style elements
	for script in soup(["script", "style","title","head","[document]"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)

	visible_text=(text.encode('utf-8'))

	FewText=visible_text[2500:3000]


	for  words in SearchWords :

		SearchPhrase=words		


		if SearchPhrase in FewText:
			insensitive_hippo = re.compile(re.escape(SearchPhrase), re.IGNORECASE)
			FewText= insensitive_hippo.sub('<b>'+SearchPhrase+'</b>',FewText)
		
		if SearchPhrase in PageTitle:
			insensitive_hippo = re.compile(re.escape(SearchPhrase), re.IGNORECASE)
			PageTitle= insensitive_hippo.sub('<b>'+SearchPhrase+'</b>',PageTitle)


	print "<a href=""%s"" style=""text-decoration:none;""> %s </a> <br>" % (URL,PageTitle)
	print "<a href=""%s"" style=""color:#0F0;"" > %s</a><br>" % (URL,URL)
	print "<p> ... %s ...</p>" % FewText

	print "<hr>"

print "</body>"
print "</html>"
con.commit()
con.close()

