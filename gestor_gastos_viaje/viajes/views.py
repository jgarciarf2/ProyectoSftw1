# viajes/views.py

from django.shortcuts import render, redirect
from .forms import RegistrarGastoForm
from .services.ControlViaje import ControlViaje
from .forms import RegistrarViajeForm
from .models.Viaje import Viaje
from .models.Gasto import Gasto
import requests



def convertir_a_pesos(valor, moneda):
    if moneda.upper() == 'COP':
        return valor
    try:
        response = requests.get(
            'https://open.er-api.com/v6/latest/{}'.format(moneda.upper()),
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            tasa = data['rates'].get('COP')
            if tasa:
                return valor * tasa
    except Exception:
        pass  

    tasa = 4000 
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
            mensaje = "Gasto registrado correctamente."
            gastos_del_dia = Gasto.objects.filter(viaje=gasto.viaje, fecha=gasto.fecha)
            total_gastado = sum(g.valor_en_pesos for g in gastos_del_dia)
            if gasto.viaje.es_internacional():
                presupuesto_diario_cop = convertir_a_pesos(gasto.viaje.presupuesto_diario, gasto.viaje.moneda)
            else:
                presupuesto_diario_cop = gasto.viaje.presupuesto_diario
            diferencia = presupuesto_diario_cop - total_gastado
            if viaje_id:
                form = RegistrarGastoForm(initial={'viaje': viaje_id})
            else:
                form = RegistrarGastoForm()
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
            return redirect('lista_viajes')
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
    gastos_por_dia = ControlViaje.reporte_gastos_por_dia(gastos)
    gastos_por_tipo = ControlViaje.reporte_gastos_por_tipo(gastos)
    return render(request, 'viajes/detalle_viaje.html', {
        'viaje': viaje,
        'gastos': gastos,
        'gastos_por_dia': gastos_por_dia,
        'gastos_por_tipo': gastos_por_tipo,
    })
