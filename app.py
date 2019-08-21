from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import atraccion

# Iniciar app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db
db = SQLAlchemy(app)
# Inicializar ma
ma = Marshmallow(app)

# Embarques Clase/Modelo
class Embarque(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    idFile = db.Column(db.Integer)
    mbl = db.Column(db.String)
    hbl = db.Column(db.String)
    buque = db.Column(db.String)
    pol = db.Column(db.String)
    pod = db.Column(db.String)
    destinoFinal = db.Column(db.String)
    viaje = db.Column(db.String)
    naviera = db.Column(db.String)
    tipo = db.Column(db.String)
    cliente = db.Column(db.String)
    cntr20DC = db.Column(db.Integer)
    cntr40DC = db.Column(db.Integer)
    cntr40HQ = db.Column(db.Integer)
    cntrLCL = db.Column(db.Integer)
    contenedores = db.Column(db.String)
    etd = db.Column(db.String)
    eta = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, idFile, mbl, hbl, buque, pol, pod, destinoFinal, viaje, naviera
                 , tipo, cliente, cntr20DC, cntr40DC, cntr40HQ, cntrLCL, contenedores,
                 etd, eta, status):
        self.idFile = idFile
        self.mbl = mbl
        self.hbl = hbl
        self.buque = buque
        self.pol = pol
        self.pod = pod
        self.destinoFinal = destinoFinal
        self.viaje = viaje
        self.naviera = naviera
        self.tipo = tipo
        self.cliente = cliente
        self.cntr20DC = cntr20DC
        self.cntr40DC = cntr40DC
        self.cntr40HQ = cntr40HQ
        self.cntrLCL = cntrLCL
        self.contenedores = contenedores
        self.etd = etd
        self.eta = eta
        self.status = status


# Embarque esquema
class EmbarqueEsquema(ma.Schema):
    class Meta:
        fields = ('idFile','mbl','hbl')

# Iniciar el esquema
embarque_esquema = EmbarqueEsquema()
embarques_esquema = EmbarqueEsquema(many = True)

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