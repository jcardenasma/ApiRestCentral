from flask import Flask, request, jsonify, make_response
from flask_basicauth import BasicAuth
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from sqlalchemy import and_
import os
import psycopg2
from functools import wraps

import atraccion
from app_db import db, ma

from Modelos.embarque import Embarque
from Modelos.embarqueTer import EmbarqueTer
from Modelos.embarqueAer import EmbarqueAer
from Modelos.factura import Factura
from Modelos.cliente import Cliente

from Esquemas.clienteEsquema import ClienteEsquema
from Esquemas.embarqueEsquema import EmbarqueEsquema
from Esquemas.embarqueTerEsquema import EmbarqueTerEsquema
from Esquemas.embarqueAerEsquema import EmbarqueAerEsquema
from Esquemas.facturaEsquema import FacturaEsquema

# Iniciar app
app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)

# Base de datos
DATABASE_URL = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kjjjlebtbphapc:45af0f19ac1cde7156fd91cd63a57ff175edc24c9d984aaf24d1bcdaf372846d@ec2-54-243-193-59.compute-1.amazonaws.com:5432/d815ljg7gaet8b'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'system'
app.config['BASIC_AUTH_PASSWORD'] = 'Sys1638'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

# Inicializar db
db.init_app(app)
# Inicializar ma
ma.init_app(app)

with app.app_context():
    db.create_all()

basic_auth = BasicAuth(app)

# Iniciar el esquema
embarque_esquema = EmbarqueEsquema()
embarques_esquema = EmbarqueEsquema(many = True)
embarqueAer_esquema = EmbarqueAerEsquema()
embarquesAer_esquema = EmbarqueAerEsquema(many = True)
embarqueTer_esquema = EmbarqueTerEsquema()
embarquesTer_esquema = EmbarqueTerEsquema(many = True)
cliente_esquema = ClienteEsquema()
clientes_esquema = ClienteEsquema(many = True)
factura_esquema = FacturaEsquema()
facturas_esquema = FacturaEsquema(many= True)

@app.route('/')
@basic_auth.required
def index():
    return '<h1>Hello world</h1>'


#Embarques Maritimos
# Crear un embarque
@app.route('/copia', methods=['GET'])
@basic_auth.required
def addEmbarque():
    solicitud = (atraccion.busquedaEmbarque())
    
    for i in solicitud:
        idFile = int(i['ID_FILE'])
        mbl = str(i['MBL'])
        hbl = str(i['HBL'])
        buque = str(i['BUQUE'])
        pol = str(i['POL'])
        pod = str(i['POD'])
        destinoFinal = str(i['DESTINO FINAL'])
        viaje = str(i['VIAJE'])
        naviera = str(i['NAVIERA'])
        tipo = str(i['TIPO'])
        cliente = str(i['CLIENTE'])
        cntr20DC = str(i['CNTR 20DC'])
        cntr40DC = str(i['CNTR 40DC'])
        cntr40HQ = str(i['CNTR 40HQ'])
        cntrLCL = str(i['CNTR LCL'])
        contenedores = str(i['CONTENEDORES'])
        etd = str(i['ETD'])
        eta = str(i['ETA'])
        status = str(i['STATUS EMBARQUES'])
        crm = str(i["_ID_CLIENTE"])
        
        nuevoEmbarque = Embarque(idFile, mbl, hbl, buque, pol, pod, destinoFinal, viaje,
                                 naviera, tipo, cliente, cntr20DC, cntr40DC, cntr40HQ, cntrLCL, 
                                 contenedores, etd, eta, status, crm)
        db.session.add(nuevoEmbarque)
        db.session.commit()
    return jsonify({'msg': 'Elementos agregados!'})


#Mandar un embarque de registro nuevo o actualizar
@app.route('/setEmbarque', methods=['POST', 'PUT'])
@basic_auth.required
def set_Embarque():
    data = request.get_json()
    if request.method == 'POST':
        db.session.add(atraccion.acomodaEmbarque(data))
        db.session.commit()
        return jsonify({'msg': 'Embarque añadido exitosamente'})
    else:
        data = request.get_json()
        busqueda = Embarque.query.filter_by(idFile = data['ID_FILE']).first()
        for key, value in data.items():
            setattr(busqueda, key, value)
        db.session.commit()
        return jsonify({'msg': 'Embarque modificado exitosamente'})


#Obtenemos todos los embarques
@app.route('/embarque', methods=['GET'])
@basic_auth.required
def get_embarques():
    all_embarques = Embarque.query.all()
    result = embarques_esquema.dump(all_embarques)
    return jsonify(result)

#Obtenemos los embarques de un solo cliente
@app.route('/embarque/<string:idCliente>')
@basic_auth.required
def get_embarquesCliente(idCliente):
    embarques = Embarque.query.filter_by(crm = idCliente).all()
    salida = embarques_esquema.dump(embarques)
    return jsonify(salida)


#Trae todos los embarques desde Filemaker
@app.route('/copiaEmb')
@basic_auth.required
def traeEmbarques():
    consultaCli = Cliente.query.all()
    resultadoCli = clientes_esquema.dump(consultaCli)
    for x in list(dict.fromkeys([i['crm'] for i in resultadoCli])):
        if len(x) > 1:
            print(x)
            carga = (atraccion.cargaEmbarques(x))
            if (carga):
                print("Embarques cargados del cliente")
    return jsonify({'msg': 'Proceso finalizado'})

        
#Elimina un embarque dado que fue terminado o cancelado
@app.route('/delEmbarque/<int:numFile>', methods=['DELETE'])
@basic_auth.required
def del_Embarque(numFile):
    busqueda = Embarque.query.filter_by(idFile = numFile).first()
    if busqueda == None:
        return jsonify({'msg': 'No existe tal embarque'})
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Embarque eliminado correctamente'})


#Embarques Terrestres
#Trae todos los embarques terrestres desde Filemaker
@app.route('/copiaEmbTer')
@basic_auth.required
def traeEmbarquesTer():
    consultaCli = Cliente.query.all()
    resultadoCli = clientes_esquema.dump(consultaCli)
    for x in list(dict.fromkeys([i['crm'] for i in resultadoCli])):
        if len(x) > 1:
            print(x)
            carga = (atraccion.cargaEmbarquesTer(x))
            if (carga):
                print("Embarques cargados del cliente")
    return jsonify({'msg': 'Proceso finalizado'})


#Obtenemos todos los embarques terrestres
@app.route('/embarqueTer', methods=['GET'])
@basic_auth.required
def get_embarquesTer():
    all_embarquesTer = EmbarqueTer.query.all()
    result = embarquesTer_esquema.dump(all_embarquesTer)
    return jsonify(result)


#Obtenemos los embarques terrestres de un solo cliente
@app.route('/embarqueTer/<string:idCliente>')
@basic_auth.required
def get_embarquesTerCliente(idCliente):
    embarquesTer = EmbarqueTer.query.filter_by(crm = idCliente).all()
    salida = embarquesTer_esquema.dump(embarquesTer)
    return jsonify(salida)    


#Mandar un registro de embarque terrestre nuevo o actualizarlo
@app.route('/setEmbarqueTer', methods=['POST', 'PUT'])
@basic_auth.required
def set_EmbarqueTer():
    data = request.get_json()
    if request.method == 'POST':
        db.session.add(atraccion.acomodaEmbarqueTer(data))
        db.session.commit()
        return jsonify({'msg': 'Embarque añadido exitosamente'})
    else:
        data = request.get_json()
        busqueda = EmbarqueTer.query.filter_by(idFileTer = data['__ID_TERRESTRE']).first()
        busqueda.operacion = data['OPERACION']
        busqueda.tipoMovimiento = data['TIPO DE MOVIMIETO']
        busqueda.cliente = data['CLIENTE']
        busqueda.origen = data['ORIGEN']
        busqueda.destino = data['DESTINO']
        busqueda.fechaCarga = data['FECHA CARGA']
        busqueda.fechaArribo = data['FECHA ARRIBO']
        busqueda.tipoCaja = data['TIPO_CAJA']      
        busqueda.crm = data['_ID_CLIENTE']
        busqueda.rutaInt = data['RUTA']
        busqueda.frontera = data['CRUCE']
        busqueda.lineanac = data['LINEA TRANSPORTISTA NACIONAL']
        busqueda.lineaint = data['LINEA TRANSPORTISTA INTERN']
        busqueda.mercancia = data['MERCANCIA']
        busqueda.fechaDescarga = data['FECHA DESCARGA']
        db.session.commit()
        return jsonify({'msg': 'Embarque modificado exitosamente'})   

#Elimina un embarque terrestre dado que fue terminado o cancelado
@app.route('/delEmbarqueTer/<string:idFileTer>', methods=['DELETE'])
@basic_auth.required
def del_EmbarqueTer(idFileTer):
    busqueda = EmbarqueTer.query.filter_by(idFileTer = idFileTer).first()
    if busqueda == None:
        return jsonify({'msg': 'No existe tal embarque'})
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Embarque eliminado correctamente'})


#Embarques Aereos
#Trae todos los embarques aereos desde Filemaker
@app.route('/copiaEmbAer')
@basic_auth.required
def traeEmbarquesAer():
    consultaCli = Cliente.query.all()
    resultadoCli = clientes_esquema.dump(consultaCli)
    for x in list(dict.fromkeys([i['crm'] for i in resultadoCli])):
        if len(x) > 1:
            print(x)
            carga = (atraccion.cargaEmbarquesAer(x))
            if (carga):
                print("Embarques cargados del cliente")
    return jsonify({'msg': 'Proceso finalizado'})


#Obtenemos todos los embarques aereos
@app.route('/embarqueAer', methods=['GET'])
@basic_auth.required
def get_embarquesAer():
    all_embarquesAer = EmbarqueAer.query.all()
    result = embarquesAer_esquema.dump(all_embarquesAer)
    return jsonify(result)


#Obtenemos los embarques aereos de un solo cliente
@app.route('/embarqueAer/<string:idCliente>')
@basic_auth.required
def get_embarquesAerCliente(idCliente):
    embarquesAer = EmbarqueAer.query.filter_by(crm = idCliente).all()
    salida = embarquesAer_esquema.dump(embarquesAer)
    return jsonify(salida)    


#Mandar un registro de embarque aereo nuevo o actualizarlo
@app.route('/setEmbarqueAer', methods=['POST', 'PUT'])
@basic_auth.required
def set_EmbarqueAer():
    data = request.get_json()
    if request.method == 'POST':
        db.session.add(atraccion.acomodaEmbarqueAer(data))
        db.session.commit()
        return jsonify({'msg': 'Embarque añadido exitosamente'})
    else:
        data = request.get_json()
        busqueda = EmbarqueAer.query.filter_by(idFileAer = data['ID_FILE_AEREO']).first()
        busqueda.idCalculo = data['ID_AEREO_EASYLOAD']        
        busqueda.shipper = data['PROVEEDOR']
        busqueda.consignatario = data['CONSIGNATARIO_HOUSE']
        busqueda.aeropuertoSalida = data['AEREOPUERTO_SALIDA']
        busqueda.origen = data['CIUDAD_SALIDA_AEROPUERTO']
        busqueda.aeropuertoDestino = data['AEREOPUERTO_DESTINO']  
        busqueda.destino = data['CIUDAD_DESTINO_AEROPUERTO']
        busqueda.awb = data['AWB']
        busqueda.hwb = data['HWB']
        busqueda.etd = data['ETD']
        busqueda.eta = data['ETA']
        busqueda.crm = data['ID_CLIENTE']
        busqueda.cliente = data['CLIENTE']
        db.session.commit()
        return jsonify({'msg': 'Embarque modificado exitosamente'})  
 

#Elimina un embarque Aereo dado que fue terminado o cancelado
@app.route('/delEmbarqueAer/<string:idFileAer>', methods=['DELETE'])
@basic_auth.required
def del_EmbarqueAer(idFileAer):
    busqueda = EmbarqueAer.query.filter_by(idFileAer = idFileAer).first()
    if busqueda == None:
        return jsonify({'msg': 'No existe tal embarque'})
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Embarque eliminado correctamente'})


#Clientes
#Copiamos todos los clientes desde filemaker
@app.route('/copiarClientes')
@basic_auth.required
def copiar_Clientes():
    atraccion.copiaClientes()
    #all_Clientes = Cliente.query.all().count()
    #result = clientes_esquema.dump(all_Clientes)
    #return jsonify(result)
    return jsonify({'msg': 'Clientes copiados exitosamente'})

#Crear un cliente
@app.route('/setCliente', methods=['POST', 'PUT'])
@basic_auth.required
def set_Cliente():
    if request.method == 'POST':
        data = request.get_json()
        newClient = Cliente(data["rfc"], data["password"], data["crm"])
        db.session.add(newClient)
        db.session.commit()
        return jsonify({'msg': 'El cliente fue agregado exitosamente'})
    else:
        data = request.get_json()
        busqueda = Cliente.query.filter_by(crm = (data['crm'])).first()
        busqueda.rfc = data['rfc']
        busqueda.password = data['password']
        db.session.commit()
        return jsonify({'msg': 'Cliente modificado exitosamente'})

#Nos traemos todos los clientes
@app.route('/getClientes')
@basic_auth.required
def get_Clientes():
    all_Clientes = Cliente.query.all()
    result = clientes_esquema.dump(all_Clientes)
    return jsonify(result)

@app.route('/restoClientes')
@basic_auth.required
def maxCliente():
    #Función para traer el max de un campo
    max_cliente = str(db.session.query(db.func.max(Cliente.crm)).scalar())
    #Lo comentado funciona, solo que nos trae el select count
    totalCliente = int(Cliente.query.count())
    #print(max_cliente)
    #atraccion.copiaClientesFaltantes(max_cliente, totalCliente)
    return jsonify({'max': max_cliente, 'total': totalCliente})


#Actualiza un cliente
@app.route('/actCliente', methods=['POST'])
@basic_auth.required
def act_cliente():
    data = request.get_json()
    busqueda = Cliente.query.filter_by(crm = data['ID_CLIENTE']).first()
    if busqueda == None:
        db.session.add(atraccion.acomodaCliente(data))
        db.session.commit()
        return jsonify({'msg': 'El cliente ha sido añadido exitosamente'})
    else:
        if busqueda.rfc == data['RFC'] and busqueda.password == data['PasswordApi']:
            return jsonify({'msg': 'El cliente se encuentra actualizado'})
        else:
            busqueda.rfc = data['RFC']
            busqueda.password = data['PasswordApi']
            db.session.commit()
            return jsonify({'msg': 'El cliente ha sido actualizado exitosamente'})


#Copia la facturas desde filemaker hacia el api
@app.route('/copiaFac')
@basic_auth.required
def traeFacturas():
    consultaCli = Cliente.query.all()
    resultadoCli = clientes_esquema.dump(consultaCli)
    for x in list(dict.fromkeys([i['crm'] for i in resultadoCli])):
        if len(x) > 1:
            print(x)
            carga = (atraccion.cargaFacturas(x))
            if (carga):
                print("Facturas cargadas del cliente")
    return jsonify({'msg': 'Proceso finalizado'})

#Permite mandar una factura nueva
@app.route('/setFactura', methods=['POST'])
@basic_auth.required
def set_Factura():
    data = request.get_json()
    db.session.add(atraccion.acomodaFactura(data))
    db.session.commit()
    return jsonify({'msg': 'Factura agregada correctamente'})

#Borra una factura en específico usando su noFact como buscador
@app.route('/delFactura/<string:factNum>', methods = ['DELETE'])
@basic_auth.required
def del_Factura(factNum):
    busqueda = Factura.query.filter_by(factNum = factNum).first()
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Factura eliminada correctamente'})

#Trae las facturas de un usuario
@app.route('/getFacturas/<string:idCliente>')
@basic_auth.required
def getFacturasCliente(idCliente):
    facturasCliente = Factura.query.filter_by(crm = idCliente).all()
    salida = facturas_esquema.dump(facturasCliente)
    return jsonify(salida)


#Traer todas las facturas de todos los usuarios
@app.route('/getTodasFacturas')
@basic_auth.required
def getAllFact():
    all_fact = Factura.query.all()
    result = facturas_esquema.dump(all_fact)
    return jsonify(result)

#Nos permite hacer el login, regresa el CRM en un JSON
@app.route('/login', methods=['POST'])
@cross_origin()
@basic_auth.required
def login():
    print("Llamada:", request)
    data = request.get_json()
    print("Cuerpo:" ,data)
    busqueda = Cliente.query.filter(Cliente.rfc == str(data['rfc']), Cliente.password == data['password']).first_or_404()
    salida = cliente_esquema.dump(busqueda)['crm']
    insert = atraccion.insertaRegistroLogin(str(data['rfc']), salida)
    return jsonify({'clave': salida})


# Correr servidor
if __name__== '__main__':
    app.run(debug=True)