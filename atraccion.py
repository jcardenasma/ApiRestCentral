from app_db import db
import requests
import json

from Modelos.embarque import Embarque
from Modelos.cliente import Cliente
from Modelos.factura import Factura

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
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ClienteNum%2CRFC%2CPasswordApi%2CID_CLIENTE%20WHERE%20STATUS%3DCLIENTE%20ORDER%20BY%20ClienteNum%20ASC'
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
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/LoginClientesApi.json?RFMfind=SELECT%20ClienteNum%2CRFC%2CPasswordApi%2CID_CLIENTE%20WHERE%20STATUS%3DCLIENTE%20AND%20ClienteNum%3E' + lastID + '%20ORDER%20BY%20ClienteNum%20ASC'
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
        print(response.status_code)
        if(response.status_code == 401 or response.status_code== 500):
                return False
        #Traemos el total de los registros para poder saber cuántos tenemos
        totalRegistros = int(response.json()['info']['foundSetCount'])

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%2CMBL%2CHBL%2CBUQUE%2CPOL%2CPOD%2C%27DESTINO FINAL%27%2CVIAJE%2CNAVIERA%2CTIPO%2CCLIENTE%2C%27CNTR 20DC%27%2C%27CNTR 40DC%27%2C%27CNTR 40HQ%27%2C%27CNTR LCL%27%2CCONTENEDORES%2CETD%2CETA%2C%27STATUS EMBARQUES%27%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm  + '%20ORDER%20BY%20ID_FILE%20ASC'

        response = requests.get(url, auth=auth_values)

        ingresados = 0
        lastID = ""
        for i in response.json()['data']:
                lastID = str(i['ID_FILE'])
                embarque = acomodaEmbarque(i)
                db.session.add(embarque)
                db.session.commit()
                ingresados += 1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(not (ingresados == totalRegistros)):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesApi.json?RFMfind=SELECT%20ID_FILE%2C_ID_CLIENTE%20WHERE%20STATUS_REPORTE%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm + '%20AND%20ID_FILE%3E' + lastID + '%20ORDER%20BY%20ID_FILE%20ASC'
                        response = requests.get(url, auth=auth_values)

                        for i in response.json()['data']:
                                lastID = str(i['ID_FILE'])
                                embarque = acomodaEmbarque(i)
                                db.session.add(embarque)
                                db.session.commit()
                                ingresados += 1
                return True

def cargaFacturas(crm):
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CFactNum%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20STATUS%3DFACTURADA%20AND%20ID_CLIENTE%3D' + crm

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)
        print(response.status_code)
        if(response.status_code == 401 or response.status_code== 500):
                return False
        #Traemos el total de los registros para poder saber cuántos tenemos
        totalRegistros = int(response.json()['info']['foundSetCount'])

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CFactNum%2CCFDI.UUID%2CID_CLIENTE%2CCERTIFICADO.FECHA%2CFILE%2CEMPRESA_QUE_FACTURARA%2CRFC%2CNombrePdf%2CXmlEncode%2CPdfEncode%2CSERIE%2CCODIGO_DIVISA%2C%27IMPORTE FACT%27%2C%27FECHA FACT%27%2CTIPO.COMPROBANTE%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20STATUS%3DFACTURADA%20AND%20ID_CLIENTE%3D' + crm  + '%20ORDER%20BY%20FactNum%20ASC'

        response = requests.get(url, auth=auth_values)

        ingresados = 0
        lastID = ""
        for i in response.json()['data']:
                lastID = str(i['FactNum'])
                factura = acomodaFactura(i)
                db.session.add(factura)
                db.session.commit()
                ingresados += 1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(not (ingresados == totalRegistros)):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CFactNum%2CCFDI.UUID%2CID_CLIENTE%2CCERTIFICADO.FECHA%2CFILE%2CEMPRESA_QUE_FACTURARA%2CRFC%2CNombrePdf%2CXmlEncode%2CPdfEncode%2CSERIE%2CCODIGO_DIVISA%2C%27IMPORTE FACT%27%2C%27FECHA FACT%27%2CTIPO.COMPROBANTE%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20STATUS%3DFACTURADA%20AND%20ID_CLIENTE%3D' + crm + '%20AND%20FactNum%3E' + lastID + '%20ORDER%20BY%20FactNum%20ASC%20LIMIT%2020'
                        response = requests.get(url, auth=auth_values)

                        print("Aqui truena, codigo ",response.status_code)
                        print("El último fue ", lastID)
                        for i in response.json()['data']:
                                lastID = str(i['FactNum'])
                                factura = acomodaFactura(i)
                                db.session.add(factura)
                                db.session.commit()
                                ingresados += 1
                return True


def acomodaFactura(respuesta):
        noFactura = str(respuesta['_NO FACTURA'])
        cfdi = str(respuesta['CFDI.UUID'])
        crm = str(respuesta['ID_CLIENTE'])
        certificadoFecha = str(respuesta['CERTIFICADO.FECHA'])
        noFile = str(respuesta['FILE'])
        empresa = str(respuesta['EMPRESA_QUE_FACTURARA'])
        rfc = str(respuesta['RFC'])
        nombrePdf = str(respuesta['NombrePdf'])
        xmlEncode = str(respuesta['XmlEncode'])
        pdfEncode = str(respuesta['PdfEncode'])
        serie = str(respuesta['SERIE'])
        codigoDivisa = str(respuesta['CODIGO_DIVISA'])
        importeFact = str(respuesta['IMPORTE FACT'])
        fechaFact = str(respuesta['FECHA FACT'])
        tipoComprobante = str(respuesta['TIPO.COMPROBANTE'])

        nuevaFactura = Factura(noFactura, cfdi, crm, certificadoFecha, noFile, empresa, rfc, nombrePdf, 
                        xmlEncode, pdfEncode, serie, codigoDivisa, importeFact, fechaFact, tipoComprobante)
        return nuevaFactura

def acomodaCliente(respuesta):
        rfc = str(respuesta['RFC'])
        password = str(respuesta['PasswordApi'])
        crm = str(respuesta['ID_CLIENTE'])

        nuevoCliente = Cliente(rfc, password, crm)

        return nuevoCliente

def acomodaEmbarque(respuesta):
        idFile = int(respuesta['ID_FILE']) if 'ID_FILE' in respuesta else " "
        mbl = str(respuesta['MBL']) if 'MBL' in respuesta else " " 
        hbl = str(respuesta['HBL']) if 'HBL' in respuesta else " "
        buque = str(respuesta['BUQUE']) if 'BUQUE' in respuesta else " "
        pol = str(respuesta['POL']) if 'POL' in respuesta else " "
        pod = str(respuesta['POD']) if 'POD' in respuesta else " "
        destinoFinal = str(respuesta['DESTINO FINAL']) if 'DESTINO FINAL' in respuesta else " "
        viaje = str(respuesta['VIAJE']) if 'VIAJE' in respuesta else " "
        naviera = str(respuesta['NAVIERA']) if 'NAVIERA' in respuesta else " "
        tipo = str(respuesta['TIPO']) if 'TIPO' in respuesta else " "
        cliente = str(respuesta['CLIENTE']) if 'CLIENTE' in respuesta else " "
        cntr20DC = int(respuesta['CNTR 20DC']) if 'CNTR 20DC' in respuesta and len(respuesta['CNTR 20DC']) > 0  else 0
        cntr40DC = int(respuesta['CNTR 40DC']) if 'CNTR 40DC' in respuesta and len(respuesta['CNTR 40DC']) > 0  else 0
        cntr40HQ = int(respuesta['CNTR 40HQ']) if 'CNTR 40HQ' in respuesta and len(respuesta['CNTR 40HQ']) > 0  else 0
        cntrLCL = int(respuesta['CNTR LCL']) if 'CNTR LCL' in respuesta and len(respuesta['CNTR LCL']) > 0  else 0
        contenedores = str(respuesta['CONTENEDORES']) if 'CONTENEDORES' in respuesta else " "
        etd = str(respuesta['ETD']) if 'ETD' in respuesta else " "
        eta = str(respuesta['ETA']) if 'ETA' in respuesta else " "
        status = str(respuesta['STATUS EMBARQUES']) if 'STATUS EMBARQUES' in respuesta else " "
        crm = str(respuesta["_ID_CLIENTE"]) if '_ID_CLIENTE' in respuesta else " "
        
        nuevoEmbarque = Embarque(idFile, mbl, hbl, buque, pol, pod, destinoFinal, viaje,
                                 naviera, tipo, cliente, cntr20DC, cntr40DC, cntr40HQ, cntrLCL, 
                                 contenedores, etd, eta, status, crm)
        
        return nuevoEmbarque