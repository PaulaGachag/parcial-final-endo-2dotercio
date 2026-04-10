import json
import pandas as pd


class CreditDataEnricher:
    def __init__(self, mock_credit_path: str):
        self.credit_data = self.load_mock(mock_credit_path)

    def load_mock(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        puntajes = []
        morosidades = []
        ultimas_consultas = []

        for cedula in df["cedula"].astype(str):
            if cedula in self.credit_data:
                data = self.credit_data[cedula]
                puntajes.append(data["puntaje_credito"])
                morosidades.append(data["morosidad"])
                ultimas_consultas.append(data["ultima_consulta"])
            else:
                puntajes.append(500)
                morosidades.append(0.5)
                ultimas_consultas.append("sin_dato")

        df["puntaje_credito"] = puntajes
        df["morosidad"] = morosidades
        df["ultima_consulta"] = ultimas_consultas

        return df