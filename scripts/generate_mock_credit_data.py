import json
import os

mock_data = {
    "1001": {"puntaje_credito": 720, "morosidad": 0.10, "ultima_consulta": "2026-04-01"},
    "1002": {"puntaje_credito": 650, "morosidad": 0.20, "ultima_consulta": "2026-04-01"},
    "1003": {"puntaje_credito": 780, "morosidad": 0.05, "ultima_consulta": "2026-04-01"},
    "1004": {"puntaje_credito": 540, "morosidad": 0.40, "ultima_consulta": "2026-04-01"},
    "1005": {"puntaje_credito": 710, "morosidad": 0.12, "ultima_consulta": "2026-04-01"},
    "1006": {"puntaje_credito": 600, "morosidad": 0.25, "ultima_consulta": "2026-04-01"},
    "1007": {"puntaje_credito": 800, "morosidad": 0.03, "ultima_consulta": "2026-04-01"},
    "1008": {"puntaje_credito": 520, "morosidad": 0.50, "ultima_consulta": "2026-04-01"},
    "1009": {"puntaje_credito": 760, "morosidad": 0.08, "ultima_consulta": "2026-04-01"},
    "1010": {"puntaje_credito": 670, "morosidad": 0.18, "ultima_consulta": "2026-04-01"}
}

output_path = "data/reference/credito_mock.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(mock_data, f, indent=2, ensure_ascii=False)

print("Mock crediticio hech")