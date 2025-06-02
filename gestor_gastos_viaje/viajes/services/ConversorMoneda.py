import requests

class ConversorMoneda:
    BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies"

    @classmethod
    def convertir(cls, origen: str, destino: str, cantidad: float) -> float:
        origen = origen.lower()
        destino = destino.lower()
        url = f"{cls.BASE_URL}/{origen}/{destino}.json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            tasa = response.json()[destino]
            return round(cantidad * tasa, 2)
        except Exception as e:
            print(f"Error en conversión de moneda: {e}")
            return 0.0
