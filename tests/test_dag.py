import pytest
from src.main import run_pipeline
from local_llm import is_local_llm_available


def test_run_pipeline_produces_outputs(monkeypatch):
    if not is_local_llm_available():
        pytest.skip("Local LLM not available")
    artifacts = run_pipeline()
    outputs = artifacts["outputs"]
    assert "faq" in outputs and outputs["faq"]["template"] == "faq"
    assert "product_page" in outputs and outputs["product_page"]["template"] == "product_page"
    assert "comparison_page" in outputs and outputs["comparison_page"]["template"] == "comparison_page"
