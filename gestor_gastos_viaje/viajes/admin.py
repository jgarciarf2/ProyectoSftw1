from django.contrib import admin
from .models.TipoGasto import TipoGasto
from .models.Viaje import Viaje
from .models.Gasto import Gasto
from .models.MetodoPago import MetodoPago

admin.site.register(TipoGasto)
admin.site.register(Viaje)
admin.site.register(Gasto)
admin.site.register(MetodoPago)