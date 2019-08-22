from app_db import db

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