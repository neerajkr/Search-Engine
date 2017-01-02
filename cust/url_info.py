import urllib2
from urlparse import urljoin
from urlparse import urlparse
import re
from time import time
import robotparser
import sqlite3
from bs4 import BeautifulSoup
import sys




hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

con=sqlite3.connect('SearchEngineDB.db')
c=con.cursor()
c.execute('''CREATE TABLE URL_INFO( URL_ID integer, SITE_ID integer,
	URL_LINK text, LAST_MODIFIED text, SECURITY_STATUS text, LOAD_TIME real , FINAL_URL_WEIGHT real)''')

weight_confg=con.cursor()


start_time=time()

NumOfGoodLink=0
NumOfHTTPerrorLink=0
NumOfFalseLink=0
NumOfTotalLink=0
NumOfLinkWithDuplicates=0

#robotparser object
rp=robotparser.RobotFileParser()


def check_web_health(root,max_depth,site_id,robot_url):    

	url_id=0
	global NumOfGoodLink
	global NumOfHTTPerrorLink
	global NumOfFalseLink
	global NumOfTotalLink
	global NumOfLinkWithDuplicates

#security check

	domain = get_domain(root)
	# print domain
	filter_domain = [domain]
	# print filter_domain

	tocrawl = [[root,1]]

	crawled = {}

	count=0;
	while tocrawl: 
		NumOfLinkWithDuplicates+=1
		crawl_ele = tocrawl.pop()
		link = crawl_ele[0]
		depth = crawl_ele[1]
		
		try:
			if link not in crawled.keys():		

				NumOfTotalLink+=1
				# print "NumOfTotalLink: ", NumOfTotalLink
				content, status = get_page(link,robot_url)

				# print content
				if status=='OK':
					NumOfGoodLink+=1
				if status=="robot files can not be accessed":
					# print "ignored because of robots.txt"
					continue			

				if content == None:
					crawled[link]= status
					if status=="Invalid Url":
						NumOfFalseLink+=1

					elif status=="Wrong Url":
						NumOfFalseLink+=1
					else:
						NumOfHTTPerrorLink+=1
					continue
					
				host = get_domain(link)
				if depth < max_depth and host in filter_domain:
					# print depth
					# print "*"*50
					outlinks = get_all_links(content,link)
					add_to_tocrawl(crawled.keys(),tocrawl, outlinks, depth+1)
				crawled[link]= status


				############### Last-modified ###################

				conn= urllib2.urlopen(urllib2.Request(link,headers=hdr)) 

				try:
					last_modified=conn.headers['last-modified']

				except Exception as e:
					last_modified="NA"

					# print "I am here ####"*5

				# print last_modified

				# print "#######"*20



				# ########### Title ################

				# soup = BeautifulSoup(conn,"lxml")                
				# PageTitle=soup.title.string

				############## HTTP/HTTPS ######### 

				if urlparse(link).scheme=="https":
					status=1
				else:
					status=0

				weight_confg.execute('SELECT FACTOR_VALUE FROM WEIGHT_CONFG WHERE FACTOR_NAME="Security_status_factor"')
				Security_status_factor=weight_confg.fetchone()[0]
				print Security_status_factor

				url_id+=1
				############# HTMl FILE DATA DOWNLOAD ###############
				

				filename=str(site_id)+"/"+str(url_id)
				# print filename
				Html_file= open(filename,"w")
				# print url_id,content
				Html_file.write(content)
				Html_file.close()

				

				############# Load Time ########################
				start_time=time()
				response = urllib2.urlopen(urllib2.Request(link,headers=hdr))
				response.read()
				end_time=time()
				response.close()
				load_time=end_time-start_time

				
				print url_id

				final_url_wt=Security_status_factor*status
				# load_time =2
				# final_url_wt = 2
				
				
				c.execute('''INSERT INTO URL_INFO( URL_ID , SITE_ID ,
				 URL_LINK , LAST_MODIFIED , SECURITY_STATUS , LOAD_TIME  , FINAL_URL_WEIGHT )VALUES(?,?,?,?,?,?,?)''',
			 (url_id,site_id,link,last_modified,status,load_time,final_url_wt))


		except :
			print "Unexpected error:", sys.exc_info()[0]
			continue




def get_domain(url):
	hostname = urlparse(url).hostname
	return hostname


def get_page(url,robot_url):
	# print url	
	# print url,robot_url
	try:

		rp.set_url(robot_url)
		rp.read()
		x=rp.can_fetch("*",url)
		# print x

		if x:   
			response = urllib2.urlopen(urllib2.Request(url,headers=hdr))

			# print response.read()
			# print "k"*100
			return response.read(), 'OK'
		else:
			return None, "robot files can not be accessed"
	except urllib2.HTTPError,e:
		return None, str(e.code)
	except urllib2.URLError,e:
				# print e.args
		return None, 'Invalid Url'
	except:
		return None, 'Wrong Url'
	
def get_next_target(page,parent):
	start_link = page.find('<a href=')
	if start_link == -1: 
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1:end_quote]
	url = urljoin(parent,url)
	return url, end_quote

def get_all_links(page,parent):
	links = []
	while True:
		url, endpos = get_next_target(page,parent)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links


def add_to_tocrawl(crawled, tocrawl, newlinks, depth):
	for link in newlinks:
		if link not in tocrawl and link not in crawled:
			tocrawl.append([link,depth])

site_id=1

robot_list=["https://www.tutorialspoint.com/robots.txt","http://www.indiabix.com/robots.txt"]


c1=con.cursor()
c1.execute('SELECT * FROM SITE_INFO')
i=0

depth=4
for row in c1  :
	site_id=row[0]
	site_url=row[1]
	robot_url=robot_list[i]
	i=i+1

	# print site_id,site_url,robot_url,i
	check_web_health(site_url,depth,site_id,robot_url)



# robot_url=robot_list[1]
# check_web_health('http://www.indiabix.com/',2,site_id,robot_url)


print NumOfTotalLink
print NumOfGoodLink
print NumOfHTTPerrorLink
print NumOfFalseLink

con.commit()
con.close()
print("-----------Total Execution Time: %s seconds"%(time()-start_time))