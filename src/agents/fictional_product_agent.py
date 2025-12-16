from typing import Dict, Any


class FictionalProductAgent:
    """Creates Product B following the ProductModel schema.
    No hidden advantages; logically comparable to Product A.
    """

    def run(self, base_schema: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "product_name": "BrightLift Vitamin C Serum",
            "concentration": base_schema["concentration"],
            "skin_type": list(base_schema["skin_type"]),
            "key_ingredients": list(base_schema["key_ingredients"]),
            "benefits": list(base_schema["benefits"]),
            "how_to_use": base_schema["how_to_use"],
            "side_effects": base_schema["side_effects"],
            "price_inr": base_schema["price_inr"],
            "schema_version": base_schema.get("schema_version", "1.0"),
        }