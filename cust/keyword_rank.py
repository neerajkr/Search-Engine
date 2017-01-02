import sqlite3

con=sqlite3.connect('SearchEngineDB.db')
c=con.cursor()
c.execute('''CREATE TABLE KEYWORD_RANK( KEYWORD	text, FILE_LOCATION  text,URL  text,TOTAL_WEIGHT  real)''')

c1=con.cursor()
c1.execute('SELECT * FROM KEYWORD_INFO')
i=0
c2=con.cursor()
c3=con.cursor()
for row in c1  :
	keyword = row[0]
	print keyword
	url_id = row[1]
	print url_id
	site_id = row[2]
	print site_id
	file_location = ("localhost/")+str(site_id)+"/"+str(url_id)
	print file_location

	try:
		c2.execute('SELECT URL_LINK FROM URL_INFO WHERE URL_ID=? AND SITE_ID=?',(url_id,site_id,))
		url = c2.fetchone()[0]
		print url
	except :
		continue

	# print type(site_id)
	c3.execute('SELECT FINAL_SITE_WEIGHT FROM SITE_INFO WHERE SITE_ID=?',(site_id,))

	site_weight = c3.fetchone()[0]
	print site_weight

	c2.execute('SELECT FINAL_URL_WEIGHT FROM URL_INFO WHERE URL_ID=? AND SITE_ID=?', (url_id,site_id,))
	url_weight = c2.fetchone()[0]
	print url_weight

	keyword_weight = row[9]


	total_weight = (site_weight) + (url_weight) + (keyword_weight)

	c.execute('''INSERT INTO KEYWORD_RANK( KEYWORD	, FILE_LOCATION  ,URL  ,TOTAL_WEIGHT  )VALUES(?,?,?,?)''',
			 (keyword,file_location,url,total_weight))

con.commit()
con.close()

   
    
    