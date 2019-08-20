from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

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
    noFactura = db.Column(db.Integer, unique = True)

    def __init__(self, noFactura):
        self.noFactura = noFactura

# Embarque esquema
class EmbarqueEsquema(ma.Schema):
    class Meta:
        fields = ('id','noFactura')

# Iniciar el esquema
embarque_esquema = EmbarqueEsquema()
embarques_esquema = EmbarqueEsquema(many = True)

# Crear un embarque
@app.route('/embarque', methods=['POST'])
def addEmbarque():
    noFact = request.json['Numero factura']

    nuevoEmbarque = Embarque(noFact)

    db.session.add(nuevoEmbarque)
    db.session.commit()

    return embarque_esquema.jsonify(nuevoEmbarque)

@app.route('/embarque', methods=['GET'])
def get_embarques():
    all_embarques = Embarque.query.all()
    result = embarques_esquema.dump(all_embarques)
    return jsonify(result)

# Correr servidor
if __name__== '__main__':
    app.run(debug=True)