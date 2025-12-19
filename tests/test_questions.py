import os
import pytest
from agents.product_parsing_agent import ProductParsingAgent
from agents.question_generation_agent import QuestionGenerationAgent
from local_llm import is_local_llm_available


def test_question_generation_min_count(monkeypatch):
    if not is_local_llm_available():
        pytest.skip("Local LLM not available")
    parser = ProductParsingAgent()
    product = parser.run({
        "product_name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": ["Oily", "Combination"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price_inr": 699,
    })
    qagent = QuestionGenerationAgent()
    qs = qagent.run(product)
    assert qs["count"] >= 15
    assert len(qs["items"]) >= 15
