from unittest import TestCase
from unittest.mock import patch

from gestor_gastos_viaje.viajes.services.ConversorMoneda import ConversorMoneda


class TestConversorMoneda(TestCase):
    @patch('gestor_gastos_viaje.viajes.services.ConversorMoneda.requests.get')
    def test_convertir_cop_a_usd(self, mock_get):
        # Simula respuesta de la API para COP a USD
        mock_get.return_value.json.return_value = {'usd': 0.00025}
        mock_get.return_value.raise_for_status = lambda: None

        resultado = ConversorMoneda.convertir('cop', 'usd', 10000)
        self.assertEqual(resultado, 2.5)

    @patch('gestor_gastos_viaje.viajes.services.ConversorMoneda.requests.get')
    def test_convertir_usd_a_cop(self, mock_get):
        # Simula respuesta de la API para USD a COP
        mock_get.return_value.json.return_value = {'cop': 4000}
        mock_get.return_value.raise_for_status = lambda: None

        resultado = ConversorMoneda.convertir('usd', 'cop', 3)
        self.assertEqual(resultado, 12000)