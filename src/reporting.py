import json
import os


def generate_report(df, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    report = {
        "total_registros": int(len(df)),
        "promedio_ingresos": float(df["ingresos"].mean()),
        "promedio_puntaje_credito": float(df["puntaje_credito"].mean()),
        "riesgo_por_categoria": df["riesgo_estimado"].value_counts().to_dict(),
        "registros": df.to_dict(orient="records"),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)