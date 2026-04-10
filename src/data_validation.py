import pandas as pd


REQUIRED_COLUMNS = [
    "cedula",
    "nombre",
    "region",
    "ingresos",
    "monto_solicitado",
    "plazo_meses",
    "historial_pagos",
]


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def validate_schema(df: pd.DataFrame) -> dict:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        return {
            "success": False,
            "message": f"Faltan columnas obligatorias: {missing}"
        }

    return {
        "success": True,
        "message": "Esquema válido"
    }


def validate_quality(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "success": False,
            "message": "El archivo está vacío"
        }

    if df["cedula"].isnull().any():
        return {
            "success": False,
            "message": "Hay cédulas nulas"
        }

    if df["cedula"].duplicated().any():
        return {
            "success": False,
            "message": "Hay cédulas duplicadas"
        }

    if (df["ingresos"] <= 0).any():
        return {
            "success": False,
            "message": "Hay ingresos inválidos"
        }

    if (df["monto_solicitado"] <= 0).any():
        return {
            "success": False,
            "message": "Hay montos solicitados inválidos"
        }

    if (df["plazo_meses"] <= 0).any():
        return {
            "success": False,
            "message": "Hay plazos inválidos"
        }

    valid_historial = ["bueno", "regular", "malo"]
    if ~df["historial_pagos"].isin(valid_historial).all():
        return {
            "success": False,
            "message": "Hay valores inválidos en historial_pagos"
        }

    return {
        "success": True,
        "message": "Calidad válida"
    }