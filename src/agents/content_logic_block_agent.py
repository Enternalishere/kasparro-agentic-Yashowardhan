from typing import Dict, Any, Callable


class ContentLogicBlockAgent:
    """Creates reusable atomic logic blocks used by templates/pages."""

    def run(self) -> Dict[str, Any]:
        registry: Dict[str, Callable[..., Any]] = {}

        def extract_benefits(product):
            return {"benefits": list(product["benefits"])}

        def usage_instructions(product):
            return {"how_to_use": product["how_to_use"]}

        def safety_notes(product):
            return {"side_effects": product["side_effects"]}

        def ingredient_summary(product):
            return {"ingredients": list(product["key_ingredients"])}

        def price_context(product):
            return {"price_inr": int(product["price_inr"])}

        def comparison_logic(a, b):
            diff = {}
            keys = [
                "product_name",
                "concentration",
                "skin_type",
                "key_ingredients",
                "benefits",
                "how_to_use",
                "side_effects",
                "price_inr",
            ]
            for k in keys:
                diff[k] = {"A": a[k], "B": b[k], "equal": a[k] == b[k]}
            return {"comparison": diff}

        registry["extract_benefits"] = extract_benefits
        registry["usage_instructions"] = usage_instructions
        registry["safety_notes"] = safety_notes
        registry["ingredient_summary"] = ingredient_summary
        registry["price_context"] = price_context
        registry["comparison_logic"] = comparison_logic

        
        return {
            "blocks": list(registry.keys()),
            "impl": registry,
        }