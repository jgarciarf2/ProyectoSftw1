from django.db import models
from datetime import date

class Viaje(models.Model):
    nombre = models.CharField(max_length=100)  # Nuevo campo
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto_diario = models.IntegerField()  # Cambiado a IntegerField
    moneda = models.CharField(max_length=10)    # Ej: COP, USD

    def es_internacional(self):
        return self.moneda.upper() != 'COP'

    def esta_activo(self):
        hoy = date.today()
        return self.fecha_inicio <= hoy <= self.fecha_fin

    def __str__(self):
        return f"{self.nombre} del {self.fecha_inicio} al {self.fecha_fin}"

    # La relación con Gasto se define en el modelo Gasto con un ForeignKey a Viaje
    # Django automáticamente permite acceder a los gastos con viaje.gasto_set.all()