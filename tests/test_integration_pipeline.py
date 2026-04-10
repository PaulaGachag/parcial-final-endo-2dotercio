import os
from src.orchestrator import PipelineOrchestrator


def test_pipeline_runs_and_creates_output():
    orchestrator = PipelineOrchestrator()
    orchestrator.run()

    assert os.path.exists("data/outputs/reporte_pipeline.json")
    assert os.path.exists("logs/execution.log")
    assert os.path.exists("data/checkpoints/checkpoint.json")