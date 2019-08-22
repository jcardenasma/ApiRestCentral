from app_db import db
import requests
import json

from Modelos.embarque import Embarque
from Modelos.cliente import Cliente

def busquedaEmbarque():
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%2CMBL%2CHBL%2CBUQUE%2CPOL%2CPOD%2C%27DESTINO FINAL%27%2CVIAJE%2CNAVIERA%2CTIPO%2CCLIENTE%2C%27CNTR 20DC%27%2C%27CNTR 40DC%27%2C%27CNTR 40HQ%27%2C%27CNTR LCL%27%2CCONTENEDORES%2CETD%2CETA%2C%27STATUS EMBARQUES%27%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3DCRM4379'

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)

        #print(response.json())
        return response.json()['data']
        #with open('prueba.json', 'w') as outfile:
                #json.dump(response.json()['data'], outfile)

def copiaClientes():
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ClienteNum%2CRFC%2CPasswordApi%2CID_CLIENTE%20WHERE%20STATUS%3DCLIENTE'
        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)

        totalRegistros = int(response.json()['info']['foundSetCount'])

        ingresados = 0
        lastID = ""

        for i in response.json()['data']:
                #print(response.json()['data'])
                lastID = str(i['ClienteNum'])
                cliente = acomodaCliente(i)
                db.session.add(cliente)
                db.session.commit()
                ingresados+=1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(not (ingresados == totalRegistros)):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ClienteNum%2CRFC%2CPasswordApi%2CID_CLIENTE%20WHERE%20STATUS%3DCLIENTE%20AND%20ClienteNum%3E' + lastID
                        response = requests.get(url, auth=auth_values)
                        for i in response.json()['data']:
                                #print(response.json()['data'])
                                lastID = str(i['ClienteNum'])
                                cliente = acomodaCliente(i)
                                db.session.add(cliente)
                                db.session.commit()
                                ingresados+=1
                return True
        return False

def copiaClientesFaltantes(maxID, totalActuales):
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ID_CLIENTE%2CRFC%2CPasswordApi%20WHERE%20STATUS%3DCLIENTE'
        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)

        totalRegistros = int(response.json()['info']['foundSetCount'])

        numeroFaltantes = totalRegistros - totalActuales

        ingresados = 0
        lastID = maxID

        print(lastID)
        while(ingresados < numeroFaltantes):
                url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ID_CLIENTE%2CRFC%2CPasswordApi%20WHERE%20STATUS%3DCLIENTE%20AND%20ID_CLIENTE%3E' + lastID
                response = requests.get(url, auth=auth_values)
                for i in response.json()['data']:
                        #print(response.json()['data'])
                        lastID = str(i['ID_CLIENTE'])
                        cliente = acomodaCliente(i)
                        db.session.add(cliente)
                        db.session.commit()
                        ingresados+=1
        return True
        

def cargaEmbarques(crm):
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)

        #Traemos el total de los registros para poder saber cuántos tenemos
        totalRegistros = response.json()['info']['foundSetCount']

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%2CMBL%2CHBL%2CBUQUE%2CPOL%2CPOD%2C%27DESTINO FINAL%27%2CVIAJE%2CNAVIERA%2CTIPO%2CCLIENTE%2C%27CNTR 20DC%27%2C%27CNTR 40DC%27%2C%27CNTR 40HQ%27%2C%27CNTR LCL%27%2CCONTENEDORES%2CETD%2CETA%2C%27STATUS EMBARQUES%27%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm

        response = requests.get(url, auth=auth_values)

        ingresados = 0
        lastID = ""
        for i in response.json()['data']:
                lastID = int(i['ID_FILE'])
                embarque = acomodaEmbarque(i)
                db.session.add(embarque)
                db.session.commit()
                ingresados += 1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(ingresados < totalRegistros):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm + '%20AND%20ID_FILE%3E' + lastID
                        response = requests.get(url, auth=auth_values)

                        for i in response.json()['data']:
                                lastID = int(i['ID_FILE'])
                                embarque = acomodaEmbarque(i)
                                db.session.add(embarque)
                                db.session.commit()
                                ingresados += 1
                return True


def acomodaCliente(respuesta):
        rfc = str(respuesta['RFC'])
        password = str(respuesta['PasswordApi'])
        crm = str(respuesta['ID_CLIENTE'])

        nuevoCliente = Cliente(rfc, password, crm)

        return nuevoCliente

def acomodaEmbarque(respuesta):
        idFile = int(respuesta['ID_FILE'])
        mbl = str(respuesta['MBL'])
        hbl = str(respuesta['HBL'])
        buque = str(respuesta['BUQUE'])
        pol = str(respuesta['POL'])
        pod = str(respuesta['POD'])
        destinoFinal = str(respuesta['DESTINO FINAL'])
        viaje = str(respuesta['VIAJE'])
        naviera = str(respuesta['NAVIERA'])
        tipo = str(respuesta['TIPO'])
        cliente = str(respuesta['CLIENTE'])
        cntr20DC = str(respuesta['CNTR 20DC'])
        cntr40DC = str(respuesta['CNTR 40DC'])
        cntr40HQ = str(respuesta['CNTR 40HQ'])
        cntrLCL = str(respuesta['CNTR LCL'])
        contenedores = str(respuesta['CONTENEDORES'])
        etd = str(respuesta['ETD'])
        eta = str(respuesta['ETA'])
        status = str(respuesta['STATUS EMBARQUES'])
        crm = str(respuesta["_ID_CLIENTE"])
        
        nuevoEmbarque = Embarque(idFile, mbl, hbl, buque, pol, pod, destinoFinal, viaje,
                                 naviera, tipo, cliente, cntr20DC, cntr40DC, cntr40HQ, cntrLCL, 
                                 contenedores, etd, eta, status, crm)
        
        return nuevoEmbarque