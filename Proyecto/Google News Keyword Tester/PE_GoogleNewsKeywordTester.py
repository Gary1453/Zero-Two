# -*- coding: utf-8 -*-
import sys
import requests
import csv
import time
import datetime
import PE_GoogleNewsQueryCreator
from bs4 import BeautifulSoup
from random import randint

head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
message = ""
fileName = input("Please type a filename for the CSV output. (Don't add .csv): ") + ".csv"
myfile = open("output/"+fileName, 'w')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
startTimeDate = datetime.datetime.now()

#Create a list(array) of Google News links based of CSV file
sourceData = input("Please enter the filename (CSV) that contains the keywords within the 'Data' folder: ")
GoogleNewsLinks = PE_GoogleNewsQueryCreator.GoogleNewsQueryCreator("data/"+sourceData) 
totalQueries = len(GoogleNewsLinks)
secondsPause = 0

#For every link in the list, verificate if the keywords return results. If not it will insert the set of keywords that were tried in another list that will be returned.
print ("Start: "+str(startTimeDate))
#try:
for link in GoogleNewsLinks:
	#Set the HTTP request
	message= ""
	r = requests.get(link[1],headers=head)
	soup = BeautifulSoup(r.content, "html.parser")
	divResultStats = soup.find_all("div",{"id":"resultStats"})
	divCaptcha = soup.find_all("input",{"id":"captcha"})
	divSearch = soup.find_all("div",{"id":"search"})
	divAnchor = []
	if len(divCaptcha) > 0:
		print (str(datetime.datetime.now()) +" - "+ "We have CAPTCHA. Renew your IP.")
		input("After renewing your IP press Enter to continue")
		divResultStats = soup.find_all("div",{"id":"resultStats"})
		divSearch = soup.find_all("div",{"id":"search"})
		divAnchor = []
		
	if len(divResultStats) == 1: 
		resultsSoup = BeautifulSoup(str(divResultStats[0]), "html.parser")
		results = resultsSoup.findAll(text='About 0 results')
		if len(results) == 1:
			message = "("+str(link[0]+1)+" of "+str(totalQueries)+")" + "I haven't found news. There are link(s) in the search engine. Please verify the keywords manually."
			GoogleNewsLinks[link[0]][len(GoogleNewsLinks[0])-1]= "Verify query results"
			wr.writerow(link)
			print (str(datetime.datetime.now()) +" - "+ message)
			continue	
		else:
			message = "("+str(link[0]+1)+" of "+str(totalQueries)+")" + " I have found news. Please verify the link provided."
			GoogleNewsLinks[link[0]][len(GoogleNewsLinks[0])-1]= "Got news"	
			wr.writerow(link)
			print (str(datetime.datetime.now()) +" - "+ message)
			continue	
	else:
		message = "("+str(link[0]+1)+" of "+str(totalQueries)+")" + " I haven't found news. " + "There are no links in the search engine."
		GoogleNewsLinks[link[0]][len(GoogleNewsLinks[0])-1]= "Discard keywords"
		wr.writerow(link)		
		print (str(datetime.datetime.now()) +" - "+ message)
		continue	
	
finalTimeDate = datetime.datetime.now()
print ("Finish: "+str(finalTimeDate))
elapsedTime = finalTimeDate - startTimeDate
divModTime = divmod(elapsedTime.days * 86400 + elapsedTime.seconds, 60)
print (str(divModTime[0])+" minute(s) and "+str(divModTime[1])+" second(s)")		