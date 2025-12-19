from typing import Dict, Any
from pydantic import ValidationError
from models import FAQPage, ProductPage, ComparisonPage, QuestionSet
from config import QA_MIN_COUNT


class FinalValidationAgent:
    def run(self, artifacts: Dict[str, Any]) -> None:
        qs = QuestionSet.model_validate(artifacts["questions"])
        if qs.count < QA_MIN_COUNT or len(qs.items) < QA_MIN_COUNT:
            raise ValueError("Insufficient questions generated")
        FAQPage.model_validate(artifacts["faq_page"])
        ProductPage.model_validate(artifacts["product_page"])
        ComparisonPage.model_validate(artifacts["comparison_page"])
