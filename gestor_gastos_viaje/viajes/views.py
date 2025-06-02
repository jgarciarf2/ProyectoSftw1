# viajes/views.py

from django.shortcuts import render, redirect
from .forms import RegistrarGastoForm
from .services.ControlViaje import ControlViaje
from .forms import RegistrarViajeForm
from .models.Viaje import Viaje
from .models.Gasto import Gasto



def convertir_a_pesos(valor, moneda):
    if moneda.upper() == 'COP':
        return valor
    # Aquí deberías llamar a la API real para obtener la tasa de cambio
    tasa = 4000  # Ejemplo: 1 USD = 4000 COP
    return valor * tasa

def registrar_gasto(request, viaje_id=None):
    mensaje = None
    diferencia = None

    if request.method == 'POST':
        form = RegistrarGastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.valor_en_pesos = convertir_a_pesos(gasto.valor_original, gasto.viaje.moneda)
            gasto.save()
            # Redirigir a la lista de viajes después de guardar
            return redirect('lista_viajes')
        else:
            mensaje = "Corrige los errores del formulario."
    else:
        if viaje_id:
            form = RegistrarGastoForm(initial={'viaje': viaje_id})
        else:
            form = RegistrarGastoForm()

    return render(request, 'viajes/registrar_gasto.html', {
        'form': form,
        'mensaje': mensaje,
        'diferencia': diferencia,
    })


def registrar_viaje(request):
    if request.method == 'POST':
        form = RegistrarViajeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_gasto')  # O a donde prefieras
    else:
        form = RegistrarViajeForm()
    return render(request, 'viajes/registrar_viaje.html', {'form': form})

def lista_viajes_con_gastos(request):
    viajes = Viaje.objects.all().prefetch_related('gastos')
    return render(request, 'viajes/lista_viajes.html', {'viajes': viajes})

def lista_viajes(request):
    viajes = Viaje.objects.all()
    return render(request, 'viajes/lista_viajes.html', {'viajes': viajes})

def detalle_viaje(request, viaje_id):
    viaje = Viaje.objects.get(id=viaje_id)
    gastos = viaje.gastos.all()
    return render(request, 'viajes/detalle_viaje.html', {'viaje': viaje, 'gastos': gastos})