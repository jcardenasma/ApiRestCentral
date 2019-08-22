from app_db import db

class Cliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key = True)
    rfc = db.Column(db.String)
    password = db.Column(db.String)
    crm = db.Column(db.String)
    embarques = db.relationship('Embarque')
    
    def __init__(self, rfc, passw, crm):
        self.rfc = rfc
        self.password = passw
        self.crm = crm
        