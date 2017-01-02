import whois
from urlparse import urlparse
import datetime
import urllib2
import sqlite3
from time import time

site_list=["https://www.tutorialspoint.com/","http://www.indiabix.com/"]


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

con=sqlite3.connect('SearchEngineDB.db')
c=con.cursor()
c.execute('''CREATE TABLE SITE_INFO( SITE_ID integer, SITE_LINK text, 
	DOMAIN_AGE integer, LOAD_TIME real,SITE_IP_LOCATION text,
	BOUNCE_RATE real,INBOUND_LIMIT integer,SITE_POPULARITY integer,NO_OF_VIEWERS integer,FINAL_SITE_WEIGHT real)''')

weight_confg=con.cursor()





def get_domain(url):
	hostname = urlparse(url).hostname
	return hostname


site_id=0
for site in site_list:
	print site
	site_id+=1




	############ Domain domain_age #############################
	domain=get_domain(site)
	print domain
	domain = whois.query(domain)
	creation_Date = domain.creation_date
	current_date=datetime.datetime.now()
	NumOfDays=current_date - creation_Date
	domain_age=NumOfDays.days
	domain_year=domain_age/365.0

	############# Load Time ########################
	start_time=time()
	response = urllib2.urlopen(urllib2.Request(site,headers=hdr))
	response.read()
	end_time=time()
	response.close()
	load_Time=end_time-start_time

	############ IP_location ###################
	site_ip_location = "localhost"

	########### Bounce_rate ################

	bounce_rate = 0
	weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="bounce_rate_factor"')
	bounce_rate_factor=weight_confg.fetchone()[0]


	########## Inbound_limit ################
	
	inbound_limit = 0
	weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Inbound_limit_factor"')
	Inbound_limit_factor=weight_confg.fetchone()[0]


	############ Site_popularity ##############
	
	site_popularity = 0	
	weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Site_popoularity_factor"')
	Site_popoularity_factor=weight_confg.fetchone()[0]


	############ N0_of_viewers ###############
	
	no_of_viewers = 0
	weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="no_viewers_factor"')
	no_viewers_factor=weight_confg.fetchone()[0]



	########## DomainAgeFactor ##########
	
	weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="DomainAgeFactor"')
	DomainAgeFactor=weight_confg.fetchone()[0]
	DomainAgeWeight=DomainAgeFactor*domain_year
	weight_confg.execute('SELECT MAX_WEIGHT FROM WEIGHT_CONFG WHERE FACTOR_NAME="DomainAgeFactor"')
	Max_weight=int(weight_confg.fetchone()[0])

	
	
	if DomainAgeWeight>Max_weight:
		DomainAgeWeight = Max_weight
	

	print DomainAgeWeight
	print DomainAgeFactor

	# print DomainAgeFactor
	# print type(DomainAgeFactor)
	# print type(domain_age)

	site_weight= DomainAgeWeight+ bounce_rate_factor*bounce_rate+Inbound_limit_factor*inbound_limit+	no_viewers_factor*no_of_viewers+Site_popoularity_factor*site_popularity
	# print site_weight

	c.execute('''INSERT INTO SITE_INFO(SITE_ID , SITE_LINK , DOMAIN_AGE , LOAD_TIME ,SITE_IP_LOCATION ,
		
	BOUNCE_RATE ,INBOUND_LIMIT ,SITE_POPULARITY ,NO_OF_VIEWERS ,FINAL_SITE_WEIGHT  )VALUES(?,?,?,?,?,?,?,?,?,?)''', (site_id,site, domain_year, load_Time,
		site_ip_location ,bounce_rate,inbound_limit,site_popularity,no_of_viewers, site_weight))


con.commit()
con.close()