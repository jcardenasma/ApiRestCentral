from app_db import ma

class FacturaEsquema(ma.Schema):
    class Model:
        fields = ('noFactura','cfdi','crm','certificadoFecha','noFile','empresa',
        'rfc','nombrePdf','xmlEncode','pdfEncode','serie','codigoDivisa','importeFact','fechaFact','tipoComprobante')