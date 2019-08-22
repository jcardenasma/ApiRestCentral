from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import os
import atraccion
from app_db import db, ma

from Modelos.embarque import Embarque
#from Modelos.factura import Factura
from Modelos.cliente import Cliente

from Esquemas.clienteEsquema import ClienteEsquema
from Esquemas.embarqueEsquema import EmbarqueEsquema

# Iniciar app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db
db.init_app(app)
# Inicializar ma
ma.init_app(app)


# Iniciar el esquema
embarque_esquema = EmbarqueEsquema()
embarques_esquema = EmbarqueEsquema(many = True)
cliente_esquema = ClienteEsquema()

# Crear un embarque
@app.route('/copia', methods=['GET'])
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
        
        nuevoEmbarque = Embarque(idFile, mbl, hbl, buque, pol, pod, destinoFinal, viaje,
                                 naviera, tipo, cliente, cntr20DC, cntr40DC, cntr40HQ, cntrLCL, contenedores, etd, eta, status)
        db.session.add(nuevoEmbarque)
        db.session.commit()
    return jsonify({'msg': 'Elementos agregados!'})

@app.route('/embarque', methods=['GET'])
def get_embarques():
    all_embarques = Embarque.query.all()
    result = embarques_esquema.dump(all_embarques)
    return jsonify(result)

# Correr servidor
if __name__== '__main__':
    app.run(debug=True)