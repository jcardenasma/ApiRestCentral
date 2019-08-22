import requests
import json

def busquedaEmbarque():
        url = 'http://fmaker.dynalias.com/RESTfm/EASYLOAD/layout/FacturasApi.json?RFMfind=SELECT%20%27_NO FACTURA%27%2CCFDI.UUID%2CCERTIFICADO.FECHA%2CFILE%2CEMPRESA_QUE_FACTURARA%2CRFC%2CNombrePdf%2CXmlEncode%2CPdfEncode%2CSERIE%2CCODIGO_DIVISA%2C%27IMPORTE FACT%27%2C%27FECHA FACT%27%2CTIPO.COMPROBANTE%20WHERE%20STATUS_PAGO%3D%27SIN PAGAR%27%20AND%20ID_CLIENTE%3DCRM4379'

        user = "system"
        password = "Sys1638"

        auth_values = (user, password)
        response = requests.get(url, auth=auth_values)

        #print(response.json())
        return response.json()['data']
        #with open('prueba.json', 'w') as outfile:
                #json.dump(response.json()['data'], outfile)
        
        