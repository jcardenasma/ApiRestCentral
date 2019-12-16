from app_db import db

# Embarques Clase/Modelo
class EmbarqueTer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    idFileTer = db.Column(db.String)
    operacion = db.Column(db.String)
    tipoMovimiento = db.Column(db.String)
    cliente = db.Column(db.String)
    origen = db.Column(db.String)
    destino = db.Column(db.String)
    fechaCarga = db.Column(db.String)
    fechaArribo = db.Column(db.String)
    tipoCaja = db.Column(db.String)
    crm = db.Column(db.String, db.ForeignKey('cliente.crm'))
    rutaInt = db.Column(db.String)
    frontera = db.Column(db.String)       
    lineanac = db.Column(db.String)
    lineaint = db.Column(db.String)
    mercancia = db.Column(db.String)
    fechaDescarga = db.Column(db.String)

    def __init__(self, idFileTer, operacion, tipoMovimiento, cliente, origen, destino, fechaCarga, fechaArribo, tipoCaja
                 , crm, rutaInt, frontera, lineanac, lineaint, mercancia, fechaDescarga):
        self.idFileTer = idFileTer
        self.operacion = operacion
        self.tipoMovimiento = tipoMovimiento
        self.cliente = cliente
        self.origen = origen
        self.destino = destino
        self.fechaCarga = fechaCarga
        self.fechaArribo = fechaArribo
        self.tipoCaja = tipoCaja
        self.crm = crm
        self.rutaInt = rutaInt
        self.frontera = frontera
        self.lineanac = lineanac
        self.lineaint = lineaint
        self.mercancia = mercancia
        self.fechaDescarga = fechaDescarga