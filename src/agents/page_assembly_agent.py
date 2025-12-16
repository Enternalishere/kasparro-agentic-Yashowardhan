from typing import Dict, Any


class PageAssemblyAgent:
    def __init__(self, logic_blocks: Dict[str, Any], templates: Dict[str, Any]):
        self.logic_blocks = logic_blocks["impl"]
        self.templates = templates["templates"]

    def build_faq_page(self, product: Dict[str, Any], questions: Dict[str, Any]) -> Dict[str, Any]:
        tpl = self.templates["faq"]
        items = questions["items"]
        faq_items = []
        # Use logic blocks to prepare supporting data
        ing = self.logic_blocks["ingredient_summary"](product)
        usage = self.logic_blocks["usage_instructions"](product)
        safety = self.logic_blocks["safety_notes"](product)

        # Produce Q&A strictly from product fields
        for q in items:
            text = q["question"]
            tl = text.lower()
            ans = None
            # Order checks to avoid accidental matches (e.g., "sensitive skin" vs generic "skin")
            if "tingling" in tl or "side effect" in tl:
                ans = product["side_effects"]
            elif "name" in tl:
                ans = product["product_name"]
            elif "10%" in tl or "concentration" in tl:
                ans = product["concentration"]
            elif "how many" in tl and "ingredient" in tl:
                ans = str(len(product["key_ingredients"]))
            elif "hyaluronic acid" in tl:
                ans = "Yes" if "Hyaluronic Acid" in product["key_ingredients"] else "No"
            elif "vitamin c" in tl and "include" in tl:
                ans = "Yes" if "Vitamin C" in product["key_ingredients"] else "No"
            elif "ingredient" in tl:
                ans = ", ".join(product["key_ingredients"]) 
            elif "benefit" in tl:
                ans = ", ".join(product["benefits"]) 
            elif "apply" in tl or "used" in tl or "drops" in tl:
                ans = product["how_to_use"]
            elif "skin" in tl:
                ans = ", ".join(product["skin_type"])
            elif "price" in tl:
                ans = str(product["price_inr"]) + " INR"
            else:
                ans = "Answerable from product data"
            faq_items.append({"q": text, "a": ans, "category": q["category"]})

        return {
            "template": "faq",
            "product": product["product_name"],
            "supporting": {**ing, **usage, **safety},
            "qa": faq_items,
        }

    def build_product_page(self, product: Dict[str, Any]) -> Dict[str, Any]:
        tpl = self.templates["product_page"]
        blocks = {
            **self.logic_blocks["extract_benefits"](product),
            **self.logic_blocks["ingredient_summary"](product),
            **self.logic_blocks["price_context"](product),
            **self.logic_blocks["usage_instructions"](product),
            **self.logic_blocks["safety_notes"](product),
        }
        return {
            "template": "product_page",
            "product": {
                "product_name": product["product_name"],
                "concentration": product["concentration"],
                "skin_type": list(product["skin_type"]),
                "key_ingredients": list(product["key_ingredients"]),
                "benefits": list(product["benefits"]),
                "how_to_use": product["how_to_use"],
                "side_effects": product["side_effects"],
                "price_inr": product["price_inr"],
            },
            "blocks": blocks,
            "meta": {"schema_version": "1.0"},
        }

    def build_comparison_page(self, a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        comparison = self.logic_blocks["comparison_logic"](a, b)
        return {
            "template": "comparison_page",
            "product_a": a["product_name"],
            "product_b": b["product_name"],
            **comparison,
        }