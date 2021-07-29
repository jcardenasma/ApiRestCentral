from app_db import db

class Cliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key = True)
    rfc = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    crm = db.Column(db.String, unique=True)
    embarques = db.relationship('Embarque')
    embarquesTer = db.relationship('EmbarqueTer')
    embarquesAer = db.relationship('EmbarqueAer')
    
    def __init__(self, username, rfc, passw, crm):
        self.rfc = rfc
        self.username = username
        self.password = passw
        self.crm = crm
        