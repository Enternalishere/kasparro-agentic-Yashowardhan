from typing import Dict, Any


class ProductParsingAgent:
    """Normalizes raw input into a ProductModel JSON structure.
    No content generation occurs here.
    """

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

    def run(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        model: Dict[str, Any] = {}
        for f in self.REQUIRED_FIELDS:
            if f not in raw_data:
                raise ValueError(f"Missing required field: {f}")
            model[f] = raw_data[f]

       
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