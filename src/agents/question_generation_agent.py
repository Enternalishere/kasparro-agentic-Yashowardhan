from typing import Dict, Any, List
import json
from local_llm import LocalLLMProvider


class QuestionGenerationAgent:
    """Generates >=15 categorized user questions answerable from product data only."""

    def run(self, product: Dict[str, Any]) -> Dict[str, Any]:
        llm = LocalLLMProvider()
        prompt = (
            "You are a product Q&A generator. Create at least 15 concise, user-centric questions "
            "about the product, grouped into categories: Informational, Usage, Safety, Purchase, Ingredients, Comparison. "
            "Only use the provided product data. Return strict JSON with keys 'count' and 'items', where 'items' is a list "
            "of objects containing 'category' and 'question'. Do not add explanations.\n"
            f"Product data: {json.dumps(product, ensure_ascii=False)}"
        )
        text = llm.chat_json(prompt)
        try:
            data = json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}") + 1
            data = json.loads(text[start:end])
        if "items" not in data or not isinstance(data["items"], list):
            raise ValueError("LLM did not return valid items list")
        return {"count": len(data["items"]), "items": data["items"]}
