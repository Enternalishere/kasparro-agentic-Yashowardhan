from typing import Dict, Any
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class FictionalProductAgent:
    """Creates Product B following the ProductModel schema."""

    def run(self, base_schema: Dict[str, Any]) -> Dict[str, Any]:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        llm = ChatOpenAI(model=model_name, temperature=0)
        prompt = (
            "Invent a realistic competitor product following the provided ProductModel schema. "
            "It must be comparable in category and price, have a different name, and reasonable variations "
            "in ingredients or benefits. Return strict JSON with keys: product_name, concentration, skin_type, "
            "key_ingredients, benefits, how_to_use, side_effects, price_inr, schema_version.\n"
            f"Base schema: {json.dumps(base_schema, ensure_ascii=False)}"
        )
        msg = HumanMessage(content=prompt)
        res = llm.invoke([msg])
        data = json.loads(res.content)
        return data
