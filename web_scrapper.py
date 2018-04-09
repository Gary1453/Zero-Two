from bs4 import BeautifulSoup
import webbrowser
import requests
import csv
import datetime
import read_excel as rd
import tesserocr
from random import randint
from PIL import Image

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

def getRucData():

	headers = { "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
	urlRuc = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
	image_url = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/captcha?accion=image&nmagic=0'

	imgFileName =  'Temporales/Imagen_' + str( randint(0, 100000) ) + '.jpeg'

	var_ruc = 10082112362

	r = requests.get( image_url , allow_redirects = True )
	
	#print (r.headers.get('content-type'))
	with open( imgFileName ,'wb') as f:

		f.write(r.content)

	imageCaptcha = Image.open( imgFileName )
	textImageCaptcha = tesserocr.file_to_text( imgFileName ).strip()

	dataRuc = { 
		
			'accion':'consPorRuc', 
			'coddist': '',
			'coddpto': '',
			'codprov': '',
			'contexto': 'ti-it',
			'nrodoc': '',
			'coddist': '',
			'razSoc': '',
			'codigo' : textImageCaptcha, 
			'nroRuc': var_ruc, 
			'tipdoc' : 1,
			'search1': var_ruc,
			'search2': '',
			'search3': '',
			'tQuery' : 'on'

			}	

	varRequ = requests.post( 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp' , data =  dataRuc , headers = headers , timeout = 5 )
	varRequ.encoding = 'utf-8'

	
	varResponse = varRequ.content
	print( varRequ.status_code )
	print( varResponse )

	#print( textImageCaptcha )


excel_file = "Proyecto/BKG_Pruebas.xlsx"
#arrRucs = rd.loadDataRuc( excel_file )

getRucData()

#dataProv = getRnpData( arrRucs )
#exportData( dataProv )

