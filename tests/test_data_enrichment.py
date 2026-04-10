import json
import pandas as pd
from src.data_enrichment import CreditDataEnricher


def test_enrich_adds_columns(tmp_path):
    mock_path = tmp_path / "mock.json"
    mock_data = {
        "1001": {
            "puntaje_credito": 700,
            "morosidad": 0.1,
            "ultima_consulta": "2026-04-01"
        }
    }

    with open(mock_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f)

    df = pd.DataFrame({"cedula": ["1001"]})
    enricher = CreditDataEnricher(str(mock_path))
    result = enricher.enrich(df)

    assert "puntaje_credito" in result.columns
    assert "morosidad" in result.columns
    assert "ultima_consulta" in result.columns


def test_enrich_uses_default_when_missing(tmp_path):
    mock_path = tmp_path / "mock.json"
    mock_data = {}

    with open(mock_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f)

    df = pd.DataFrame({"cedula": ["9999"]})
    enricher = CreditDataEnricher(str(mock_path))
    result = enricher.enrich(df)

    assert result.loc[0, "puntaje_credito"] == 500
    assert result.loc[0, "morosidad"] == 0.5