import requests
import json

def busquedaEmbarque():
    url = "http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2CMBL%2CHBL%2CBUQUE%2CPOL%2CPOD%2C%27DESTINO FINAL%27%2CVIAJE%2CNAVIERA%2CTIPO%2CCLIENTE%2C%27CNTR 20DC%27%2C%27CNTR 40DC%27%2C%27CNTR 40HQ%27%2C%27CNTR LCL%27%2CCONTENEDORES%2CETD%2CETA%2C%27STATUS EMBARQUES%27%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3DCRM4379"

    user = "system"
    password = "Sys1638"

    auth_values = (user, password)
    response = requests.get(url, auth=auth_values)

    #print(response.json())
    return response.json()['data']
    #with open('prueba.json', 'w') as outfile:
        #json.dump(response.json()['data'], outfile)
        