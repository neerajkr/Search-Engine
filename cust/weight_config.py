import sqlite3


con=sqlite3.connect('SearchEngineDB.db')
c=con.cursor()
c.execute('''CREATE TABLE WEIGHT_CONFG( FACTOR_NAME text ,FACTOR_VALUE real, MAX_WEIGHT text)''')



c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Keyword_body_factor",1,"4"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Title_name_factor",3,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Meta_Description_factor",2,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Meta_keywords_factor",2,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("url_name_factor",5,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("url_name_with_site_name_factor",2,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("H1_heading_name_factor",0.5,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("H2_heading_name_factor",0.5,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Site_quality_factor",1,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Link_quality_factor",1,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("bounce_rate_factor",1,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Inbound_limit_factor",1,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("no_viewers_factor",1,"NA"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Security_status_factor",1,"NA"))


c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("Site_popoularity_factor",1,"NA"))


c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("DomainAgeFactor",1,"3"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("image_tag_factor",0.01,"1"))

c.execute('''INSERT INTO WEIGHT_CONFG( FACTOR_NAME  ,FACTOR_VALUE , MAX_WEIGHT   )VALUES(?,?,?)''',
			 ("anchor_tag_factor",0.01,"1"))





con.commit()
con.close()


