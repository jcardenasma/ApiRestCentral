from app_db import ma
from Modelos.cliente import Cliente

class ClienteEsquema(ma.Schema):
    class Meta:
        fields = ('rfc', 'password', 'crm')