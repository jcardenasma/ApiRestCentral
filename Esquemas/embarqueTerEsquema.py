from app_db import ma
from Modelos.embarqueTer import EmbarqueTer

# Embarque esquema
class EmbarqueTerEsquema(ma.Schema):
    class Meta:
        fields = ('idFileTer','operacion','tipoMovimiento', 'cliente', 'origen', 'destino', 'fechaCarga', 'fechaArribo', 'tipoCaja',
                  'crm', 'rutaInt', 'frontera', 'lineanac', 'lineaint', 'mercancia', 'fechaDescarga')