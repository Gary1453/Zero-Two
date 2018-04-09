#Importing CSV module
import csv
def GoogleNewsQueryCreator(dataPath):

	#Creating an list(array) based on a CSV file
	sheet = list(csv.reader(open(dataPath)))

	#Declaring an empty list that will contain the Google News links with keywords included and field that will be populated with the action to take.
	cols, rows = len(sheet[0])+3, len(sheet)
	GoogleNewsLinks = [[0 for x in range(cols)] for y in range(rows)] 
	keywords= ""

	#Populating the GoogleNewsLinks
	for row in range(0,len(sheet)):
		GoogleNewsLinks[row][0] = row
		for col in range(0,len(sheet[0])):		
			
			if (col < len(sheet[0])-1):
				keywords = keywords + '"'+(sheet[row][col])+'"+'
				GoogleNewsLinks[row][col+2] = sheet[row][col]
				
			else:
				keywords = keywords + '"'+(sheet[row][col])+'"'
				GoogleNewsLinks[row][col+2] = sheet[row][col]
		GoogleNewsLinks[row][1] = "https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q="+keywords
		keywords= ""
		
	return GoogleNewsLinks