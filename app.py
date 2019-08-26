from flask import Flask, request, jsonify, make_response
from flask_basicauth import BasicAuth
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from sqlalchemy import and_
import os
from functools import wraps

import atraccion
from app_db import db, ma

from Modelos.embarque import Embarque
from Modelos.factura import Factura
from Modelos.cliente import Cliente

from Esquemas.clienteEsquema import ClienteEsquema
from Esquemas.embarqueEsquema import EmbarqueEsquema
from Esquemas.facturaEsquema import FacturaEsquema

# Iniciar app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'system'
app.config['BASIC_AUTH_PASSWORD'] = 'Sys1638'
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
cliente_esquema = ClienteEsquema()
clientes_esquema = ClienteEsquema(many = True)
factura_esquema = FacturaEsquema()
facturas_esquema = FacturaEsquema(many= True)

@app.route('/')
@basic_auth.required
def index():
    return '<h1>Hello world</h1>'


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

@app.route('/embarque', methods=['GET'])
@basic_auth.required
def get_embarques():
    all_embarques = Embarque.query.all()
    result = embarques_esquema.dump(all_embarques)
    return jsonify(result)

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
        busqueda = Embarque.query.filter_by(idFile = data['ID_FILE']).first()
        busqueda = atraccion.acomodaEmbarque(data)
        db.session.commit()
        return jsonify({'msg': 'Embarque modificado exitosamente'})

#Elimina un embarque dado que fue terminado o cancelado
@app.route('/delEmbarque/<int:numFile>', methods=['DELETE'])
@basic_auth.required
def del_Embarque(numFile):
    busqueda = Embarque.query.filter_by(idFile = numFile).first()
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Embarque eliminado correctamente'})


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

@app.route('/delFactura/<int:noFact>', methods = ['DELETE'])
@basic_auth.required
def del_Factura(noFact):
    busqueda = Factura.query.filter_by(noFactura = noFact).first()
    db.session.delete(busqueda)
    db.session.commit()
    return jsonify({'msg': 'Factura eliminada correctamente'})

#Traer todas las facturas de todos los usuarios
@app.route('/getTodasFacturas')
@basic_auth.required
def getAllFact():
    all_fact = Factura.query.all()
    result = facturas_esquema.dump(all_fact)
    return jsonify(result)


@app.route('/login', methods=['GET'])
@cross_origin()
#@basic_auth.required
def login():
    print("Llamada:", request)
    data = request.get_json()
    print("Cuerpo:" ,data)
    busqueda = Cliente.query.filter(Cliente.rfc == str(data['rfc']), Cliente.password == data['password']).first_or_404()
    salida = cliente_esquema.dump(busqueda)['crm']
    return jsonify({'clave': salida})


# Correr servidor
if __name__== '__main__':
    app.run(debug=True)