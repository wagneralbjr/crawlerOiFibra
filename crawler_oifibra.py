import requests
import csv


URL_API = "https://www.oi.com.br/ccstorex/custom/v1/serviceConsultaCepFibra/ConsultaCepFibra"

CAMINHO = 'statewide.csv'


def request_json(URL, params):
	resultado = requests.post(URL, params)
	return resultado.json()

def le_base_zips(caminho):
	
	with open(caminho) as csvfile:
	
		linhas = csv.DictReader(csvfile)
		return list(set([linha['POSTCODE'].replace('-','') for linha in linhas]))

	return None
print('lendoBase')
baseZipCodes = le_base_zips(CAMINHO)

print('baseLida')
for zip in baseZipCodes:
	resultado = request_json(URL_API, { 'postalCode': zip , 'streetNumber': 10}) 
	viabilidade = False
	if 'viabilities' in resultado.keys():
		viabilidade = True
	
	print( zip,'\t', viabilidade ) 
		



