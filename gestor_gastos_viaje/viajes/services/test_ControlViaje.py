import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_gastos_viaje.settings')
django.setup()

import unittest
from unittest.mock import MagicMock, patch
from datetime import date

from gestor_gastos_viaje.viajes.services.ControlViaje import ControlViaje


class TestControlViaje(unittest.TestCase):
    def setUp(self):
        # Mock Viaje
        self.viaje_activo = MagicMock()
        self.viaje_activo.esta_activo.return_value = True
        self.viaje_activo.es_internacional.return_value = True
        self.viaje_activo.moneda = "usd"
        self.viaje_activo.presupuesto_diario = 1000
        self.viaje_activo.gastos.filter.return_value = []

        self.viaje_inactivo = MagicMock()
        self.viaje_inactivo.esta_activo.return_value = False

        # Mock MetodoPago y TipoGasto
        self.metodo_efectivo = MagicMock()
        self.metodo_efectivo.nombre = "Efectivo"
        self.metodo_tarjeta = MagicMock()
        self.metodo_tarjeta.nombre = "Tarjeta"
        self.tipo_gasto = MagicMock()
        self.tipo_gasto.nombre = "Comida"

    @patch('gestor_gastos_viaje.viajes.services.ControlViaje.Gasto')
    @patch('gestor_gastos_viaje.viajes.services.ConversorMoneda.ConversorMoneda.convertir', return_value=5000)
    def test_registrar_gasto_exitoso(self, mock_convertir, mock_gasto):
        fecha = date.today()
        mock_gasto.objects.create.return_value.valor_en_pesos = 5000
        mock_gasto.objects.create.return_value.viaje = self.viaje_activo

        gasto = ControlViaje.registrar_gasto(self.viaje_activo, fecha, 10, self.metodo_efectivo, self.tipo_gasto)
        self.assertEqual(gasto.valor_en_pesos, 5000)
        self.assertEqual(gasto.viaje, self.viaje_activo)

    def test_registrar_gasto_viaje_inactivo(self):
        fecha = date.today()
        with self.assertRaises(Exception) as cm:
            ControlViaje.registrar_gasto(self.viaje_inactivo, fecha, 10, self.metodo_efectivo, self.tipo_gasto)
        self.assertIn("El viaje no está activo", str(cm.exception))

    def test_reporte_gastos_por_dia(self):
        gasto1 = MagicMock()
        gasto1.fecha = date.today()
        gasto1.metodo_pago.nombre = "Efectivo"
        gasto1.valor_en_pesos = 100

        gasto2 = MagicMock()
        gasto2.fecha = date.today()
        gasto2.metodo_pago.nombre = "Tarjeta"
        gasto2.valor_en_pesos = 200

        gastos = [gasto1, gasto2]
        reporte = ControlViaje.reporte_gastos_por_dia(gastos)
        self.assertEqual(reporte[gasto1.fecha]['Efectivo'], 100)
        self.assertEqual(reporte[gasto2.fecha]['Tarjeta'], 200)
        self.assertEqual(reporte[gasto1.fecha]['Total'], 300)

    def test_reporte_gastos_por_tipo(self):
        gasto1 = MagicMock()
        gasto1.tipo_gasto.nombre = "Comida"
        gasto1.metodo_pago.nombre = "Efectivo"
        gasto1.valor_en_pesos = 100

        gasto2 = MagicMock()
        gasto2.tipo_gasto.nombre = "Comida"
        gasto2.metodo_pago.nombre = "Tarjeta"
        gasto2.valor_en_pesos = 200

        gastos = [gasto1, gasto2]
        reporte = ControlViaje.reporte_gastos_por_tipo(gastos)
        self.assertEqual(reporte["Comida"]['Efectivo'], 100)
        self.assertEqual(reporte["Comida"]['Tarjeta'], 200)
        self.assertEqual(reporte["Comida"]['Total'], 300)

    def test_diferencia_presupuesto_diario(self):
        fecha = date.today()
        gasto1 = MagicMock()
        gasto1.valor_en_pesos = 200
        self.viaje_activo.gastos.filter.return_value = [gasto1]
        self.viaje_activo.presupuesto_diario = 1000

        diferencia = ControlViaje.diferencia_presupuesto_diario(self.viaje_activo, fecha)
        self.assertEqual(diferencia, 800)

if __name__ == "__main__":
    unittest.main()