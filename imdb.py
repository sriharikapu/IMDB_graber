import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import sys

req = requests.get("http://www.imdb.com/chart/top")
page = req.text
soup = BeautifulSoup(page, 'html.parser')
# print (soup.prettify())

imdb = soup.find(class_="lister-list")

# get top 250 movie names and years
movie_names = []
movie_year = [0] * 250

j = 1
for i in range(250):
 content = str(soup.findAll('td', {'class':'titleColumn'})[i])

 name = re.findall ( '>(.*?)</a>', content)
 movie_names.insert(len(movie_names), name)
    
 year = str(soup.findAll('span', {'class':'secondaryInfo'})[i])
 movie_year[i] = int(re.findall(r"\(([0-9_]+)\)", year)[0])
 
 #progress checker Takes about 1 min
 print('Recieved ' + str(j) + ' movies') 
 j = j+1

# Now storing the list in a text file
f = open("movie_list.txt", "w+")
for i in range(250):
	f.write(str(movie_names[i]) + "\t" + str(movie_year[i]) + "\n")

#Using Pandas
m_name = [mn.get_text() for mn in imdb.select(".titleColumn a")]
m_year = [my.get_text() for my in imdb.select(".secondaryInfo")]
wow = pd.DataFrame({
    "Release Year":m_year,
    "Movie Name": m_name
     })
print(wow)