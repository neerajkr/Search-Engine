import os
import re
import urllib
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import sqlite3

tokenizer = RegexpTokenizer(r'\w+')

# paths = [1,2]

con=sqlite3.connect('SearchEngineDB.db')
c=con.cursor()
c.execute('''CREATE TABLE KEYWORD_INFO( KEYWORDS text, URL_ID integer,
		 SITE_ID integer, FREQ_IN_BODY integer, FREQ_IN_TITLE integer, FREQ_IN_META_DESCRPTN integer ,FREQ_IN_META_KEYWORD integer,
		 URLNAME_WEIGHT integer, H1_WEIGHT integer, FINAL_FREQ_WEIGHT real)''')


weight_confg=con.cursor()
site_object=con.cursor()
url_obj=con.cursor()



weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Title_name_factor"')
Title_name_factor=weight_confg.fetchone()[0]
# print "Title_name_factor" ,Title_name_factor

weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Keyword_body_factor"')
Keyword_body_factor=weight_confg.fetchone()[0]
# print "Keyword_body_factor" , Keyword_body_factor

weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Meta_Description_factor"')
Meta_Description_factor=weight_confg.fetchone()[0]
# print "Meta_Description_factor",Meta_Description_factor

weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Meta_keywords_factor"')
Meta_keywords_factor=weight_confg.fetchone()[0]
# print "Meta_keywords_factor",Meta_keywords_factor

weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="url_name_factor"')
url_name_factor=weight_confg.fetchone()[0]
# print "url_name_factor",url_name_factor


weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="H1_heading_name_factor"')
H1_heading_name_factor=weight_confg.fetchone()[0]
# print "H1_heading_name_factor", H1_heading_name_factor

weight_confg.execute('SELECT MAX_WEIGHT FROM WEIGHT_CONFG WHERE FACTOR_NAME="Keyword_body_factor"')
MaxKeywordBodyWt=int(weight_confg.fetchone()[0])
# print "MaxKeywordBodyWt", MaxKeywordBodyWt



site_object.execute('SELECT * FROM SITE_INFO')
for row in site_object:
	for filename in os.listdir(str(row[0])):

		FilePath=str(row[0])+"/"+str(filename)
		try:
			html = urllib.urlopen(FilePath).read()    #HTML content
		except :
			continue
		

		soup = BeautifulSoup(html,"lxml")

		# print "filename", filename
# ################# Header Extraction #########################

		HeaderSoup = soup.findAll('h1')
		if HeaderSoup:
			Header=HeaderSoup[0].encode('utf-8')
		else:
			Header=""

		ToknizedHeader=Header.lower()

# 		print ToknizedHeader

# ################# MetaKey Extraction #########################

		descKey=soup.findAll(attrs={"name":"Keywords"})
		if descKey:
			descKey=descKey[0]['content'].encode('utf-8')
		else:
			descKey=""
		ToknizedMetaKey=descKey.lower()

# 		print ToknizedMetaKey


# ################# MetaDes Extraction #########################
	
		descKey=soup.findAll(attrs={"name":"Description"})
		if descKey:
			descKey=descKey[0]['content'].encode('utf-8')
		else:
			descKey=""
		ToknizedMetaDes=descKey.lower()






################## Pre-Processing Of Text ###############################

		# kill all script and style elements
		for script in soup(["script", "style"]):
		    script.extract()    # rip it out

		text = soup.get_text()

		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)	


####################### Tekenizing Words ###############################
		ToknizedWords=tokenizer.tokenize(text)
		TotalNumberOfWords=len(ToknizedWords)
		ToknizedWords=[x.lower() for x in ToknizedWords]  ####### converting all the words in lowercase
		cnt = Counter(ToknizedWords)
		words = re.findall('\w+', open('SmartStoplist.txt').read().lower())		


#################### Frequnecy Count #############

		for word in ToknizedWords:
			word=word.lower()
			if word in words:
				continue
			else: 
				cnt[word] += 1

		############## Title of Page ##################

		PageTitle=soup.title
		# print "*"*25

		if PageTitle and PageTitle.string:
			PageTitle=PageTitle.string
			PageTitle= PageTitle.lower()
		else:
			PageTitle=""

			

		
		# PageTitle=soup.title
		# # print "*"*25

		# if PageTitle and PageTitle.string:
		# 	ToknizedPageTitle=tokenizer.tokenize(PageTitle.string)
		# else:
		# 	PageTitle=""
		# 	ToknizedPageTitle=tokenizer.tokenize(PageTitle)			
		# # print ToknizedPageTitle
		# ToknizedPageTitleCounter=Counter(ToknizedPageTitle)
		# # print ToknizedPageTitleCounter

		###################### URL-NAME ########################


		try:
			url_obj.execute('SELECT URL_LINK FROM URL_INFO WHERE URL_ID=?',(filename,))
			# print filename
			url_link=url_obj.fetchone()[0]
			url_link=url_link.lower()
		except :
			continue

		# print "*"*25
####################### filling the table ##################

		for word, count in cnt.items():
			Weight=0
			TitleFreq=0
			url_name_wt=0
			heading_wt=0
			Meta_Description_wt=0
			Meta_keywords_wt=0	

			try:
				if word in url_link:
					url_name_wt=1
				if word in PageTitle:
					TitleFreq=1
				if word in ToknizedMetaKey:
					Meta_keywords_wt=1
				if word in ToknizedMetaDes:
					Meta_Description_wt=1
				if word in ToknizedHeader:
					heading_wt=1
				
				



		################### Weight calculation ###################


				################ KeywordBodyPct ##################
				KeywordBodyPct=((count*1.0)/TotalNumberOfWords)*100
				KeywordBodyWt=KeywordBodyPct*Keyword_body_factor
				if KeywordBodyWt> MaxKeywordBodyWt:
					KeywordBodyWt=MaxKeywordBodyWt

				Weight=KeywordBodyWt+TitleFreq*Title_name_factor+url_name_factor*url_name_wt+H1_heading_name_factor*heading_wt+Meta_Description_factor*Meta_Description_wt+Meta_keywords_factor*Meta_keywords_wt
				
				SITEID=row[0]
				

				c.execute('''INSERT INTO KEYWORD_INFO( KEYWORDS , URL_ID ,
			 SITE_ID , FREQ_IN_BODY , FREQ_IN_TITLE , FREQ_IN_META_DESCRPTN  , FREQ_IN_META_KEYWORD, URLNAME_WEIGHT , H1_WEIGHT ,
			 FINAL_FREQ_WEIGHT  )VALUES(?,?,?,?,?,?,?,?,?,?)''',
			  (word,filename,SITEID,count,TitleFreq,Meta_Description_wt ,Meta_keywords_wt,url_name_wt,heading_wt ,Weight))


				
				
			except Exception as e:
				pass

con.commit()
con.close()
	
