from typing import Dict, Any, Union
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class ProductParsingAgent:
    """Normalizes raw input into a ProductModel JSON structure."""

    REQUIRED_FIELDS = [
        "product_name",
        "concentration",
        "skin_type",
        "key_ingredients",
        "benefits",
        "how_to_use",
        "side_effects",
        "price_inr",
    ]

    def run(self, raw_data: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        if isinstance(raw_data, str):
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            llm = ChatOpenAI(model=model_name, temperature=0)
            prompt = (
                "Extract a ProductModel JSON from the following unstructured text. "
                "Keys: product_name, concentration, skin_type (list), key_ingredients (list), benefits (list), "
                "how_to_use, side_effects, price_inr (integer). Return strict JSON only.\n"
                f"Text: {raw_data}"
            )
            msg = HumanMessage(content=prompt)
            res = llm.invoke([msg])
            data = json.loads(res.content)
        else:
            data = dict(raw_data)
        model: Dict[str, Any] = {}
        for f in self.REQUIRED_FIELDS:
            if f not in data:
                raise ValueError(f"Missing required field: {f}")
            model[f] = data[f]

       
        model["product_name"] = str(model["product_name"]).strip()
        model["concentration"] = str(model["concentration"]).strip()
        model["skin_type"] = list(model["skin_type"]) 
        model["key_ingredients"] = list(model["key_ingredients"]) 
        model["benefits"] = list(model["benefits"])  
        model["how_to_use"] = str(model["how_to_use"]).strip()
        model["side_effects"] = str(model["side_effects"]).strip()
        model["price_inr"] = int(model["price_inr"]) 
        model["schema_version"] = "1.0"
        return model
