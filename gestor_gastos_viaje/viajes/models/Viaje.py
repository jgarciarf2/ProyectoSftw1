from django.db import models
from datetime import date

class Viaje(models.Model):
    nombre = models.CharField(max_length=100) 
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto_diario = models.IntegerField() 
    moneda = models.CharField(max_length=10)    

    def es_internacional(self):
        return self.moneda.upper() != 'COP'

    def esta_activo(self):
        hoy = date.today()
        return self.fecha_inicio <= hoy <= self.fecha_fin

    def __str__(self):
        return f"{self.nombre} ( {self.fecha_inicio} - {self.fecha_fin} ) - {self.moneda}"

