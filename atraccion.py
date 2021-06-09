from app_db import db
import requests
import json

from Modelos.embarqueTer import EmbarqueTer
from Modelos.embarqueAer import EmbarqueAer
from Modelos.embarque import Embarque
from Modelos.cliente import Cliente
from Modelos.factura import Factura


def insertaRegistroLogin(rfc):
        url = "http://appfm.dynalias.com/RESTfm/EASYLOADEMONUEVO/bulk/RegistroApi.json"

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        dataJson = {"RFC": "BME820202JM6"  }
        print(dataJson)

        response =  requests.post(url, auth=auth_values, data=dataJson)
        return response.json()['data']

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


def cargaEmbarquesTer(crm):
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesTerApi.json?RFMfind=SELECT%20__ID_TERRESTRE%2C_ID_CLIENTE%20WHERE%20STATUS%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)
        print(response.status_code)
        if(response.status_code == 401 or response.status_code== 500):
                return False
        #Traemos el total de los registros para poder saber cuántos tenemos
        totalRegistros = int(response.json()['info']['foundSetCount'])

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesTerApi.json?RFMfind=SELECT%20__ID_TERRESTRE%2C_ID_CLIENTE%2COPERACION%2C%27TIPO DE MOVIMIETO%27%2CCLIENTE%2C%27ORIGEN%27%2CDESTINO%2C%27FECHA CARGA%27%2C%27FECHA ARRIBO%27%2CTIPO_CAJA%2CRUTA%2CCRUCE%2C%27LINEA TRANSPORTISTA NACIONAL%27%2C%27LINEA TRANSPORTISTA INTERN%27%2CMERCANCIA%2C%27FECHA DESCARGA%27%20WHERE%20STATUS%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm  + '%20ORDER%20BY%20ID_TERRESTRE_NUM%20ASC'

        response = requests.get(url, auth=auth_values)

        ingresados = 0
        lastID = ""
        for i in response.json()['data']:
                lastID = str(i['__ID_TERRESTRE'])
                embarqueTer = acomodaEmbarqueTer(i)
                db.session.add(embarqueTer)
                db.session.commit()
                ingresados += 1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(not (ingresados == totalRegistros)):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarquesTerApi.json?RFMfind=SELECT%20__ID_TERRESTRE%2C_ID_CLIENTE%20WHERE%20STATUS%3DACTIVA%20AND%20_ID_CLIENTE%3D' + crm + '%20AND%20__ID_TERRESTRE%3D' + lastID + '%20ORDER%20BY%20ID_TERRESTRE_NUM%20ASC'
                        response = requests.get(url, auth=auth_values)

                        for i in response.json()['data']:
                                lastID = str(i['__ID_TERRESTRE'])
                                embarqueTer = acomodaEmbarqueTer(i)
                                db.session.add(embarqueTer)
                                db.session.commit()
                                ingresados += 1
                return True
                                


def cargaEmbarquesAer(crm):
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarqueAerApi.json?RFMfind=SELECT%20ID_AEREO_EASYLOAD%2CID_FILE_AEREO%2CID_CLIENTE%20WHERE%20STATUS_FILE%3DACTIVA%20AND%20ID_CLIENTE%3D' + crm

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)
        print(response.status_code)
        if(response.status_code == 401 or response.status_code== 500):
                return False
        #Traemos el total de los registros para poder saber cuántos tenemos
        totalRegistros = int(response.json()['info']['foundSetCount'])

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarqueAerApi.json?RFMfind=SELECT%20ID_AEREO_EASYLOAD%2CID_FILE_AEREO%2CPROVEEDOR%2CCONSIGNATARIO_HOUSE%2CPO%2CAEREOPUERTO_SALIDA%2CCIUDAD_SALIDA_AEROPUERTO%2CAEREOPUERTO_DESTINO%2CCIUDAD_DESTINO_AEROPUERTO%2CAWB%2CHWB%2CETD%2CETA%2CID_CLIENTE%2CCLIENTE%20WHERE%20STATUS_FILE%3DACTIVA%20AND%20ID_CLIENTE%3D' + crm  + '%20ORDER%20BY%20ID_FILE_AEREO_NUM%20ASC'

        response = requests.get(url, auth=auth_values)

        ingresados = 0
        lastID = ""
        for i in response.json()['data']:
                lastID = str(i['ID_FILE_AEREO'])
                embarqueAer = acomodaEmbarqueAer(i)
                db.session.add(embarqueAer)
                db.session.commit()
                ingresados += 1
        
        if ingresados == totalRegistros:
                return True
        else:
                while(not (ingresados == totalRegistros)):
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/EmbarqueAerApi.json?RFMfind=SELECT%20ID_AEREO_EASYLOAD%2CID_FILE_AEREO%2CID_CLIENTE%20WHERE%20STATUS_FILE%3DACTIVA%20AND%20ID_CLIENTE%3D' + crm + '%20AND%20ID_FILE_AEREO%3D' + lastID + '%20ORDER%20BY%20ID_FILE_AEREO_NUM%20ASC'
                        response = requests.get(url, auth=auth_values)

                        for i in response.json()['data']:
                                lastID = str(i['ID_FILE_AEREO'])
                                embarqueAer = acomodaEmbarqueAer(i)
                                db.session.add(embarqueAer)
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

        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CFactNum%2CCFDI.UUID%2CID_CLIENTE%2CCERTIFICADO.FECHA%2CFILE%2CEMPRESA_QUE_FACTURARA%2CRFC%2CNombrePdf%2CXmlEncode%2CPdfEncode%2CSERIE%2CCODIGO_DIVISA%2C%27IMPORTE FACT%27%2C%27FECHA FACT%27%2CTIPO.COMPROBANTE%2C%27PLACE OF RECEIPT%27%2C%27PORT OF LOADING%27%2C%27PORT OF DISCHARGE%27%2C%27PLACE OF DELIVERY%27%2CFECHA_PAGO%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20STATUS%3DFACTURADA%20AND%20ID_CLIENTE%3D' + crm  + '%20ORDER%20BY%20FactNum%20ASC'

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
                        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CFactNum%2CCFDI.UUID%2CID_CLIENTE%2CCERTIFICADO.FECHA%2CFILE%2CEMPRESA_QUE_FACTURARA%2CRFC%2CNombrePdf%2CXmlEncode%2CPdfEncode%2CSERIE%2CCODIGO_DIVISA%2C%27IMPORTE FACT%27%2C%27FECHA FACT%27%2CTIPO.COMPROBANTE%2C%27PLACE OF RECEIPT%27%2C%27PORT OF LOADING%27%2C%27PORT OF DISCHARGE%27%2C%27PLACE OF DELIVERY%27%2CFECHA_PAGO%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20STATUS%3DFACTURADA%20AND%20ID_CLIENTE%3D' + crm + '%20AND%20FactNum%3E' + lastID + '%20ORDER%20BY%20FactNum%20ASC%20LIMIT%2020'
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
        cfdi = str(respuesta['CfdiUuid'])
        crm = str(respuesta['ID_CLIENTE'])
        certificadoFecha = str(respuesta['CertificadoFecha'])
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
        tipoComprobante = str(respuesta['TipoComprobante'])
        factNum = str(respuesta['FactNum'])
        placeReceipt = str(respuesta['PLACE OF RECEIPT'])
        portLoading = str(respuesta['PORT OF LOADING'])
        portDischarge = str(respuesta['PORT OF DISCHARGE'])
        placeDelivery = str(respuesta['PLACE OF DELIVERY'])
        fechaPago = str(respuesta['FECHA_PAGO'])

        nuevaFactura = Factura(noFactura, cfdi, crm, certificadoFecha, noFile, empresa, rfc, nombrePdf, 
                        xmlEncode, pdfEncode, serie, codigoDivisa, importeFact, fechaFact, tipoComprobante, factNum,
                        placeReceipt, portLoading, portDischarge, placeDelivery, fechaPago)
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


def acomodaEmbarqueTer(respuesta):
        idFileTer = str(respuesta['__ID_TERRESTRE']) if '__ID_TERRESTRE' in respuesta else " "
        operacion = str(respuesta['OPERACION']) if 'OPERACION' in respuesta else " " 
        tipoMovimiento = str(respuesta['TIPO DE MOVIMIETO']) if 'TIPO DE MOVIMIETO' in respuesta else " "
        cliente = str(respuesta['CLIENTE']) if 'CLIENTE' in respuesta else " "
        origen = str(respuesta['ORIGEN']) if 'ORIGEN' in respuesta else " "
        destino = str(respuesta['DESTINO']) if 'DESTINO' in respuesta else " "
        fechaCarga = str(respuesta['FECHA CARGA']) if 'FECHA CARGA' in respuesta else " "
        fechaArribo = str(respuesta['FECHA ARRIBO']) if 'FECHA ARRIBO' in respuesta else " "
        tipoCaja = str(respuesta['TIPO_CAJA']) if 'TIPO_CAJA' in respuesta else " "
        crm = str(respuesta["_ID_CLIENTE"]) if '_ID_CLIENTE' in respuesta else " "
        rutaInt = str(respuesta['RUTA']) if 'RUTA' in respuesta else " "
        frontera = str(respuesta['CRUCE']) if 'CRUCE' in respuesta else " "
        lineanac = str(respuesta['LINEA TRANSPORTISTA NACIONAL']) if 'LINEA TRANSPORTISTA NACIONAL' in respuesta else " "
        lineaint = str(respuesta['LINEA TRANSPORTISTA INTERN']) if 'LINEA TRANSPORTISTA INTERN' in respuesta else " "
        mercancia = str(respuesta['MERCANCIA']) if 'MERCANCIA' in respuesta else " "
        fechaDescarga = str(respuesta['FECHA DESCARGA']) if 'FECHA DESCARGA' in respuesta else " "        

        nuevoEmbarqueTer = EmbarqueTer(idFileTer, operacion, tipoMovimiento, cliente, origen, destino, fechaCarga, fechaArribo,
                                 tipoCaja, crm, rutaInt, frontera, lineanac, lineaint, mercancia, fechaDescarga)
        
        return nuevoEmbarqueTer       

def acomodaEmbarqueAer(respuesta):
        idFileAer = str(respuesta['ID_FILE_AEREO']) if 'ID_FILE_AEREO' in respuesta else " "
        idCalculo = str(respuesta['ID_AEREO_EASYLOAD']) if 'ID_AEREO_EASYLOAD' in respuesta else " "        
        shipper = str(respuesta['PROVEEDOR']) if 'PROVEEDOR' in respuesta else " " 
        consignatario = str(respuesta['CONSIGNATARIO_HOUSE']) if 'CONSIGNATARIO_HOUSE' in respuesta else " "
        aeropuertoSalida = str(respuesta['AEREOPUERTO_SALIDA']) if 'AEREOPUERTO_SALIDA' in respuesta else " "
        origen = str(respuesta['CIUDAD_SALIDA_AEROPUERTO']) if 'CIUDAD_SALIDA_AEROPUERTO' in respuesta else " "
        aeropuertoDestino = str(respuesta['AEREOPUERTO_DESTINO']) if 'AEREOPUERTO_DESTINO' in respuesta else " "
        destino = str(respuesta['CIUDAD_DESTINO_AEROPUERTO']) if 'CIUDAD_DESTINO_AEROPUERTO' in respuesta else " "
        awb = str(respuesta['AWB']) if 'AWB' in respuesta else " "
        hwb = str(respuesta['HWB']) if 'HWB' in respuesta else " "  
        etd = str(respuesta['ETD']) if 'ETD' in respuesta else " "
        eta = str(respuesta['ETA']) if 'ETA' in respuesta else " "
        crm = str(respuesta['ID_CLIENTE']) if 'ID_CLIENTE' in respuesta else " "
        cliente = str(respuesta['CLIENTE']) if 'CLIENTE' in respuesta else " "  
            

        nuevoEmbarqueAer = EmbarqueAer(idFileAer, idCalculo, shipper, consignatario, aeropuertoSalida, origen,
        aeropuertoDestino, destino, awb, hwb, etd, eta, crm, cliente)
        
        return nuevoEmbarqueAer  

