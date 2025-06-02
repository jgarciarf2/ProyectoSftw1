from django.db import models
from .Viaje import Viaje
from .MetodoPago import MetodoPago
from .TipoGasto import TipoGasto

class Gasto(models.Model):
    viaje = models.ForeignKey(Viaje, related_name='gastos', on_delete=models.CASCADE)
    fecha = models.DateField()
    valor_original = models.FloatField()      # valorOriginal
    valor_en_pesos = models.FloatField()      # valorPesos
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    tipo_gasto = models.ForeignKey(TipoGasto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.valor_original} {self.viaje.moneda} el {self.fecha}"