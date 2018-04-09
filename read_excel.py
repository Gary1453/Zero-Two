import pandas as pd
import numpy as np
import os

#Funciones para trabajar data en excel

def loadDataRuc( excelFile ):

	df1 = pd.read_excel( excelFile , sheet_name = 0 , index_col = None , na_values = ['NA'] )
	ruc_list = df1['RUC']

	return ruc_list

"""
current_directory = os.getcwd()
bkg_excel = "Proyecto/BKG_Pruebas.xlsx"
ruc_array = loadDataRuc( bkg_excel)

print( ruc_array )
"""