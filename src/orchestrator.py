import json
import os
import time
from datetime import datetime

from src.data_validation import load_data, validate_schema, validate_quality
from src.data_processing import transform_data
from src.data_enrichment import CreditDataEnricher
from src.reporting import generate_report


class PipelineOrchestrator:
    def __init__(self):
        self.input_path = "data/raw/solicitudes_credito.csv"
        self.mock_path = "data/reference/credito_mock.json"
        self.output_path = "data/outputs/reporte_pipeline.json"
        self.log_path = "logs/execution.log"
        self.checkpoint_path = "data/checkpoints/checkpoint.json"

        os.makedirs("logs", exist_ok=True)
        os.makedirs("data/checkpoints", exist_ok=True)
        os.makedirs("data/outputs", exist_ok=True)

    def log_json(self, level: str, message: str, extra: dict | None = None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "extra": extra or {}
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def save_checkpoint(self, stage: str):
        checkpoint = {
            "last_stage": stage,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

    def retry(self, func, *args, **kwargs):
        delays = [0.5, 1]

        for attempt, delay in enumerate(delays, start=1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_json(
                    "WARNING",
                    f"Intento {attempt} fallido",
                    {"error": str(e)}
                )
                time.sleep(delay)

        return func(*args, **kwargs)

    def run(self):
        try:
            self.log_json("INFO", "Inicio del pipeline")

            df = self.retry(load_data, self.input_path)
            self.save_checkpoint("load_data")
            self.log_json("INFO", "Datos cargados")

            schema_result = validate_schema(df)
            if not schema_result["success"]:
                raise ValueError(schema_result["message"])
            self.save_checkpoint("validate_schema")
            self.log_json("INFO", "Esquema validado")

            quality_result = validate_quality(df)
            if not quality_result["success"]:
                raise ValueError(quality_result["message"])
            self.save_checkpoint("validate_quality")
            self.log_json("INFO", "Calidad validada")

            df = transform_data(df)
            self.save_checkpoint("transform_data")
            self.log_json("INFO", "Transformación completada")

            enricher = CreditDataEnricher(self.mock_path)
            df = enricher.enrich(df)
            self.save_checkpoint("enrich_data")
            self.log_json("INFO", "Enriquecimiento completado")

            generate_report(df, self.output_path)
            self.save_checkpoint("generate_report")
            self.log_json("INFO", "Reporte generado", {"output": self.output_path})

            self.log_json("INFO", "Pipeline completado exitosamente")

        except FileNotFoundError as e:
            self.log_json("ERROR", "Archivo no encontrado", {"error": str(e)})
            raise
        except KeyError as e:
            self.log_json("ERROR", "Clave no encontrada", {"error": str(e)})
            raise
        except ValueError as e:
            self.log_json("ERROR", "Error de validación", {"error": str(e)})
            raise
        except Exception as e:
            self.log_json("ERROR", "Error inesperado", {"error": str(e)})
            raise


if __name__ == "__main__":
    orchestrator = PipelineOrchestrator()
    orchestrator.run()