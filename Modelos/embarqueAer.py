from app_db import db

# Embarques Clase/Modelo
class EmbarqueAer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    idFileAer = db.Column(db.String)
    idCalculo = db.Column(db.String)    
    shipper = db.Column(db.String)
    consignatario = db.Column(db.String)
    aeropuertoSalida = db.Column(db.String)
    origen = db.Column(db.String)
    aeropuertoDestino = db.Column(db.String)
    destino = db.Column(db.String)
    awb = db.Column(db.String)
    hwb = db.Column(db.String)
    etd = db.Column(db.String)
    eta = db.Column(db.String)
    crm = db.Column(db.String, db.ForeignKey('cliente.crm'))
    cliente = db.Column(db.String)

    def __init__(self, idFileAer, idCalculo, shipper, consignatario, aeropuertoSalida, origen, aeropuertoDestino, destino, 
                 awb, hwb, etd, eta, crm, cliente):
        self.idFileAer = idFileAer
        self.idCalculo = idCalculo
        self.shipper = shipper
        self.consignatario = consignatario
        self.aeropuertoSalida = aeropuertoSalida
        self.origen = origen
        self.aeropuertoDestino = aeropuertoDestino
        self.destino = destino
        self.awb = awb
        self.hwb = hwb
        self.etd = etd
        self.eta = eta
        self.crm = crm
        self.cliente = cliente