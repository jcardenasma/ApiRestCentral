from app_db import db

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    noFactura = db.Column(db.String)
    cfdi = db.Column(db.String)
    crm = db.Column(db.String, db.ForeignKey('cliente.crm'))
    certificadoFecha = db.Column(db.String)
    noFile = db.Column(db.String)
    empresa = db.Column(db.String)
    rfc = db.Column(db.String)
    nombrePdf = db.Column(db.String)
    xmlEncode = db.Column(db.String)
    pdfEncode = db.Column(db.String)
    serie = db.Column(db.String)
    codigoDivisa = db.Column(db.String)
    importeFact = db.Column(db.String)
    fechaFact = db.Column(db.String)
    tipoComprobante = db.Column(db.String)

    def __init__(self, noFactura, cfdi, crm, certificadoFecha, noFile, empresa, rfc, 
                    nombrePdf, xmlEncode, pdfEncode, serie, codigoDivisa, importeFact, fechaFact, tipoComprobante):
        self.noFactura = noFactura
        self.cfdi = cfdi
        self.crm = crm
        self.certificadoFecha = certificadoFecha
        self.noFile = noFile
        self.empresa = empresa
        self.rfc = rfc
        self.nombrePdf = nombrePdf
        self.xmlEncode = xmlEncode
        self.pdfEncode = pdfEncode
        self.serie = serie
        self.codigoDivisa = codigoDivisa
        self.importeFact = importeFact
        self.fechaFact = fechaFact
        self.tipoComprobante = tipoComprobante
        