from ..models.Viaje import Viaje
from ..models.Gasto import Gasto
from ..services.ConversorMoneda import ConversorMoneda
from collections import defaultdict


class ControlViaje:

    @staticmethod
    def registrar_gasto(viaje: Viaje, fecha, valor, metodo_pago, tipo_gasto):
        if not viaje.esta_activo():
            raise Exception("El viaje no está activo, no se pueden registrar gastos.")

        # Conversión de moneda
        if viaje.es_internacional():
            valor_en_pesos = ConversorMoneda.convertir(viaje.moneda, "cop", valor)
        else:
            valor_en_pesos = valor

        # Crear y guardar el gasto
        gasto = Gasto.objects.create(
            viaje=viaje,
            fecha=fecha,
            valor_original=valor,
            valor_en_pesos=valor_en_pesos,
            metodo_pago=metodo_pago,
            tipo_gasto=tipo_gasto,
        )
        return gasto

    @staticmethod
    def reporte_gastos_por_dia(gastos):
        gastos_por_dia = defaultdict(lambda: {'Efectivo': 0, 'Tarjeta': 0, 'Total': 0})
        for gasto in gastos:
            metodo = 'Efectivo' if 'efectivo' in gasto.metodo_pago.nombre.lower() else 'Tarjeta'
            gastos_por_dia[gasto.fecha][metodo] += gasto.valor_en_pesos
            gastos_por_dia[gasto.fecha]['Total'] += gasto.valor_en_pesos
        return dict(gastos_por_dia)

    @staticmethod
    def reporte_gastos_por_tipo(gastos):
        gastos_por_tipo = defaultdict(lambda: {'Efectivo': 0, 'Tarjeta': 0, 'Total': 0})
        for gasto in gastos:
            metodo = 'Efectivo' if 'efectivo' in gasto.metodo_pago.nombre.lower() else 'Tarjeta'
            tipo = gasto.tipo_gasto.nombre
            gastos_por_tipo[tipo][metodo] += gasto.valor_en_pesos
            gastos_por_tipo[tipo]['Total'] += gasto.valor_en_pesos
        return dict(gastos_por_tipo)

    @staticmethod
    def diferencia_presupuesto_diario(viaje: Viaje, fecha):
        gastos_del_dia = viaje.gastos.filter(fecha=fecha)
        total_gastado = sum(g.valor_en_pesos for g in gastos_del_dia)
        return round(viaje.presupuesto_diario - total_gastado, 2)
