import requests
from multiprocessing import Process,Pool
import asyncio
from aiohttp import ClientSession
import csv


url_api = "https://www.oi.com.br/ccstorex/custom/v1/serviceConsultaCepFibra/ConsultaCepFibra"

def verifica_disponivel(CEP, casa = 0, stateInitials = 'XX'):
    """ Esta função verifica se existe viabilidade da oi fibra na região.
        Não vi ainda enviando parametro de stateInitials diferente de XX
        A casa se marca a opção sem número, envia o valor 0 na casa.
    """

    params = { 'postalCode': CEP, "streetNumber" : casa, "stateInitials": stateInitials}
    
    r = requests.post(url_api, data = params)
    print(r.json())
    if ('status' in r.json().keys()):
        disponivel = False 
    else:
        disponivel = True

    return disponivel

def le_ceps( caminho ) :
    
    with open('ceps_tratados.csv') as csvfile : 
        spamreader = csv.reader(csvfile, delimiter= ',')
        ceps = [x[2].replace('-','') for x in spamreader]

    return ceps

# disp = verifica_disponivel('72225016')
# print(disp)
# disp = verifica_disponivel('72225031')
# print(disp)

ceps = le_ceps('ceps_tratados.csv')
#print(ceps)
#ceps = [ '72225031']

async def fetch(url, session, CEP):
    #print(CEP)
    casa = '0'
    stateInitials = 'XX'
    try :
        async with session.post(url, data={ 'postalCode': CEP, "streetNumber" : casa, "stateInitials": stateInitials} ) as response:
            jsonAnswer = await response.json()
            disponivel = False if 'status' in jsonAnswer.keys() else True
            return {'cep': CEP, 'disponivel': disponivel}
    except:
        # se entrou na exceção marca como falso.
        return {'cep': CEP, 'disponivel': False}

async def bound_fetch(sem, url, session, CEP):
    #getter function with semaphore

    async with sem:
        return await fetch(url, session, CEP)

def write_csv(respostas):

    #recebe como entrada um array de dicionarios.
    dict_resultado = {}
    for elem in respostas :
        dict_resultado[ elem['cep'] ] = elem['disponivel']

    #le o csv antigo para fazer a nova base.
    # adiciona a informação da disponibilidade ou não.

    base_final = []
    with open('ceps_tratados.csv') as csvfile : 
        spamreader = csv.reader(csvfile, delimiter= ',')
        for row in spamreader:
            cep_linha = row[2].replace('-','')
            if cep_linha in dict_resultado:
                disponivel = 'sim' if dict_resultado[cep_linha] else 'nao'
            else:
                disponivel = 'nao'
        
            base_final.append( [row[0] , row[1], row[2], disponivel ] )
    

    base_final[0][3] = 'fibra_disp'
    #escreve o csv com a base tratada.
    with open('csv_final.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
        
        #spamwriter.writerow(['LON','LAT','POSTCODE'])
        for row in base_final:
            spamwriter.writerow(row)

async def run():
    url = url_api
    tasks = []

    sem = asyncio.Semaphore(300)
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for cep in ceps[1:]: #pula header.
            task = asyncio.ensure_future(bound_fetch(sem ,url_api, session, cep))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        #print(responses)
    
    #chama a função que escreve a resposta dos csvs.
    write_csv(responses)

number = 10000

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run())
loop.run_until_complete(future)



