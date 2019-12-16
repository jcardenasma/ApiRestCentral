from app_db import ma
from Modelos.embarqueAer import EmbarqueAer

# Embarque esquema
class EmbarqueAerEsquema(ma.Schema):
    class Meta:
        fields = ('idFileAer','shipper', 'consignatario', 'aeropuertoSalida', 'origen', 'aeropuertoDestino', 'destino', 'awb',
                  'hwb', 'etd', 'eta', 'crm', 'cliente')