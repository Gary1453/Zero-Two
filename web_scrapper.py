from bs4 import BeautifulSoup
import webbrowser
import requests
import csv
import datetime
import read_excel as rd
import tesserocr
from random import randint
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from io import BytesIO
#import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#webbrowser.open()

"""
Funciones a Implementar 
"""

def exportData( rucs ):
	
	now = datetime.datetime.now()
	nombreFile = 'export/output_' + str(now.day) + '_'+ str(now.month) +  '_' + str(now.year) + '_' + str(now.hour) +  '_' + str(now.minute)  +  '_' + str(now.second)

	f = open( nombreFile , 'w')

	with f :
		
		writer = csv.writer(f)

		for row in rucs:
			writer.writerow(row)

def getRnpData( arrRucs ):

	headers = { "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

	urlProvIns = 'http://www.osce.gob.pe/consultasenlinea/rnp_consulta/ProveedoresInscritos.asp?action=enviar' 

	arrRucs = arrRucs[0:5]
	output = []

	for ruc in arrRucs:

	#ruc = '20101093027'
		data = []
		soupData_ = ''
		num_rows = 0
		temp = []
		temp_index = 0
		dataProvIns = { 
			
				'cmbCapitulo':'', 
				'cmbTipoPersona' : '' , 
				'txtRnp': '' , 
				'txtRuc' : ruc 

				}

		varRequ = requests.post( urlProvIns , data =  dataProvIns , headers = headers , timeout = 5 )
		varRequ.encoding = 'utf-8'

		varResponse = varRequ.content
		soup = BeautifulSoup(varRequ.content, 'html.parser')

		try:

			soupData_ = ( soup.find_all('table')[2] ).find_all('td' , { 'class' : 'TDData'} )
			num_rows =  len( ( soup.find_all('table')[2] ).find_all('tr') ) - 4

			print( "RUC: " + str(ruc) )
			#print( "num: " + str(num_rows) )
			
			for dataValue in soupData_:
				data.append(str(dataValue.text))
			
			for index in range(num_rows):

				temp = data[ temp_index : temp_index + 13 ]
				temp_index = temp_index + 13
				output.append(temp)
			

		except IndexError as IndexException:
			
			#print ( IndexException )			
			print ( "El RUC " + str(ruc) + " no tiene proveedores asginados")				

	#13 columns for a file 	
	#print( varRequ.status_code )
	#print( soup.prettify() )
	#print(  soupData_ )
	return output

def getRucData( var_ruc ):
	
	headers = { "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

	imgFileName =  'Temporales/Imagen_' + str( randint(0, 100000) ) + '.png'
	url = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
	driver = webdriver.Chrome()
	driver.maximize_window()
	driver.get( url )

	driver.implicitly_wait(5)

	driver.switch_to_frame("leftFrame")
	driver.find_element_by_name('search1').send_keys( var_ruc )

	img = driver.find_element_by_tag_name('img')
	loc = img.location
	size = img.size	


	png = driver.get_screenshot_as_png()
	temp = Image.open(BytesIO(png))

	left = loc['x']
	top = loc['y']
	right = loc['x'] + size['width']
	bottom = loc['y'] + size['height']

	temp = temp.crop((left, top, right, bottom)) 
	temp.save(imgFileName) 				
	
	imageCaptcha = Image.open( imgFileName )
	textImageCaptcha = tesserocr.file_to_text( imgFileName ).strip()

	driver.find_element_by_name('codigo').send_keys( textImageCaptcha )
	driver.find_element_by_css_selector('.form-button').click()
	#driver.quit() 
	
	driver.switch_to.default_content()
	#driver.refresh()

	

	driver.switch_to_frame("mainFrame")

	temp = driver.find_elements_by_tag_name("td")
	
	data = []
	#row = { 'index' :  , 'value' : }


	for i in range(41):
		"""
		if temp[i].text.strip() != '':
			if i%2 != 0:
				
				row['value'] =  temp[i].text.strip()
				data.append( row )

			else :

				row = { 'index' : '' , 'value' : '' }
				row['index'] =  temp[i].text.strip()
		"""
		if temp[i].text.strip() != '':
			data.append( (temp[i].text).strip() )

	print( data )

	#print( imgFileName )
	#print( textImageCaptcha )

#excel_file = "Proyecto/BKG_Pruebas.xlsx"
#arrRucs = rd.loadDataRuc( excel_file )

getRucData(10082112362)

#dataProv = getRnpData( arrRucs )
#exportData( dataProv )

