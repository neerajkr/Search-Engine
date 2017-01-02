# Search-Engine

Search Engine
--------------------


-----------------------------------------------
Basic Requirements to run the code:-
There should be linux operating system  installed in the system.
It should have python 2.7 version.
Sqlite browser should be installed.
Apache server should be configured to support python script.
------------------------------------------------------------------------
---------------------------------------------------------------------------
Steps to run the code:-
1.Run the program weight_config.py
  Commands to run on the terminal:-
  Go to the folder in which the file is located.
  Type Python weight_config.py
  Output:-A file with the name SearchEnginge.db with a database table WEIGHT_CONFG
---------------------------------------------------------------------------------------
2.Run the program site_info.py
  Commands to run on the terminal:-
  Go to the folder in which the file is located.
  Type Python site_info.py
  Output:-A database table SITE_INFO will be created in the database file SearchEnginge.db
---------------------------------------------------------------------------------------------
3.Run the program url_info.py
  Commands to run on the terminal:-
  Go to the folder in which the file is located.
  Type Python url_info.py
  Output:-A database table URl_INFO will be created in the databse file SearchEnginge.db
--------------------------------------------------------------------------------------------------
4.Run the program keyword_info.py
  Commands to run on the terminal:-
  Go to the folder in which the file is located.
  Type Python keyword_info.py
  Output:-A database table KEYWORD_INFO will be created in the database file SearchEnginge.db
------------------------------------------------------------------------------------------------------
5.Run the program keyword_rank.py
  Commands to run on the terminal:-
  Go to the folder in which the file is located.
  Type Python keyword_rank.py
  Output:-A database table KEYWORD_RANK will be created in the database file SearchEnginge.db
---------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
Location of the files:-
File                     Location
search.html              /var/www/html
weight_config.py         /usr/lib/cgi-bin
site_info.py             /usr/lib/cgi-bin
url_info.py              /usr/lib/cgi-bin
keyword_info.py          /usr/lib/cgi-bin
keyword_rank.py          /usr/lib/cgi-bin
search.py                /usr/lib/cgi-bin
-----------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
Steps for running the search engine:-
Start the apache server.
Type in the browser localhost/search.html.
A searchbox will appear.
Enter the query that you want to search
A web page containing the results will appear.


