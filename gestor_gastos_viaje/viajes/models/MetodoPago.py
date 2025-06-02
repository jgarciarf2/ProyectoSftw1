from django.db import models

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
