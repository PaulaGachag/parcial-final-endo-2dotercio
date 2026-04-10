import pandas as pd
from src.data_validation import validate_schema, validate_quality


def test_validate_schema_ok():
    df = pd.DataFrame({
        "cedula": [1],
        "nombre": ["Ana"],
        "region": ["Centro"],
        "ingresos": [2000000],
        "monto_solicitado": [3000000],
        "plazo_meses": [12],
        "historial_pagos": ["bueno"]
    })
    result = validate_schema(df)
    assert result["success"] is True


def test_validate_schema_missing_column():
    df = pd.DataFrame({
        "cedula": [1],
        "nombre": ["Ana"]
    })
    result = validate_schema(df)
    assert result["success"] is False


def test_validate_quality_empty():
    df = pd.DataFrame(columns=[
        "cedula", "nombre", "region", "ingresos",
        "monto_solicitado", "plazo_meses", "historial_pagos"
    ])
    result = validate_quality(df)
    assert result["success"] is False


def test_validate_quality_duplicate_cedula():
    df = pd.DataFrame({
        "cedula": [1, 1],
        "nombre": ["Ana", "Luis"],
        "region": ["Centro", "Norte"],
        "ingresos": [2000000, 3000000],
        "monto_solicitado": [3000000, 4000000],
        "plazo_meses": [12, 10],
        "historial_pagos": ["bueno", "regular"]
    })
    result = validate_quality(df)
    assert result["success"] is False


def test_validate_quality_ok():
    df = pd.DataFrame({
        "cedula": [1, 2],
        "nombre": ["Ana", "Luis"],
        "region": ["Centro", "Norte"],
        "ingresos": [2000000, 3000000],
        "monto_solicitado": [3000000, 4000000],
        "plazo_meses": [12, 10],
        "historial_pagos": ["bueno", "regular"]
    })
    result = validate_quality(df)
    assert result["success"] is True