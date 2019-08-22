from app_db import db

class Cliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key = True)
    rfc = db.Column(db.String)
    password = db.Column(db.String)
    crm = db.Column(db.String)
    nombre = db.Column(db.String, db.ForeignKey('embarque.cliente'), nullable= False)
    
    def __init__(self, idCliente, rfc, passw, crm):
        self.idCliente = idCliente
        self.rfc = rfc
        self.password = passw
        self.crm = crm
        