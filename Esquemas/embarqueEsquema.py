from app_db import ma
from Modelos.embarque import Embarque

# Embarque esquema
class EmbarqueEsquema(ma.Schema):
    class Meta:
        fields = ('idFile','mbl','hbl', 'buque', 'pol', 'pod', 'destinoFinal', 'viaje', 'naviera',
                  'tipo', 'cliente', 'cntr20DC', 'cntr40DC', 'cntr40HQ', 'cntrLCL', 'contenedores',
                  'etd', 'eta', 'status')