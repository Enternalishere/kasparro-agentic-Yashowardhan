from typing import Dict, Any
import json
from local_llm import LocalLLMProvider


class FictionalProductAgent:
    """Creates Product B following the ProductModel schema."""

    def run(self, base_schema: Dict[str, Any]) -> Dict[str, Any]:
        llm = LocalLLMProvider()
        prompt = (
            "Invent a realistic competitor product following the provided ProductModel schema. "
            "It must be comparable in category and price, have a different name, and reasonable variations "
            "in ingredients or benefits. Return strict JSON with keys: product_name, concentration, skin_type, "
            "key_ingredients, benefits, how_to_use, side_effects, price_inr, schema_version.\n"
            f"Base schema: {json.dumps(base_schema, ensure_ascii=False)}"
        )
        text = llm.chat_json(prompt)
        data = json.loads(text)
        return data
