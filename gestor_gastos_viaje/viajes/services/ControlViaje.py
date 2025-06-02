from ..models.Viaje import Viaje
from ..models.Gasto import Gasto
from ..services.ConversorMoneda import ConversorMoneda

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
    def diferencia_presupuesto_diario(viaje: Viaje, fecha):
        gastos_del_dia = viaje.gastos.filter(fecha=fecha)
        total_gastado = sum(g.valor_en_pesos for g in gastos_del_dia)
        return round(viaje.presupuesto_diario - total_gastado, 2)
