from django.db import models

class TipoGasto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
