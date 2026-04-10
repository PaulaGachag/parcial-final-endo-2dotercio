import pandas as pd


def calcular_cuota_mensual(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cuota_mensual_estimada"] = (df["monto_solicitado"] / df["plazo_meses"]).round(2)
    return df


def categorizar_riesgo(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def riesgo(row):
        if row["historial_pagos"] == "malo":
            return "alto"
        if row["historial_pagos"] == "regular":
            return "medio"
        return "bajo"

    df["riesgo_estimado"] = df.apply(riesgo, axis=1)
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = calcular_cuota_mensual(df)
    df = categorizar_riesgo(df)
    return df