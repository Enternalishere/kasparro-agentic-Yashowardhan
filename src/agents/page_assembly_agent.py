from typing import Dict, Any, List, Tuple
from local_llm import LocalLLMProvider


class PageAssemblyAgent:
    def __init__(self, logic_blocks: Dict[str, Any], templates: Dict[str, Any]):
        self.logic_blocks = logic_blocks["impl"]
        self.templates = templates["templates"]
        self._corpus_cache: Dict[str, Tuple[List[Tuple[str, str, str]], np.ndarray]] = {}

    def build_faq_page(self, product: Dict[str, Any], questions: Dict[str, Any]) -> Dict[str, Any]:
        items = questions["items"]
        faq_items = []
        ing = self.logic_blocks["ingredient_summary"](product)
        usage = self.logic_blocks["usage_instructions"](product)
        safety = self.logic_blocks["safety_notes"](product)
        llm = LocalLLMProvider()
        docs: List[Tuple[str, str, str]] = []
        docs.append(("product_name", product["product_name"], f"Product name: {product['product_name']}"))
        docs.append(("concentration", product["concentration"], f"Concentration: {product['concentration']}"))
        docs.append(("skin_type", ", ".join(product["skin_type"]), f"Skin types: {', '.join(product['skin_type'])}"))
        docs.append(("key_ingredients", ", ".join(product["key_ingredients"]), f"Key ingredients: {', '.join(product['key_ingredients'])}"))
        docs.append(("benefits", ", ".join(product["benefits"]), f"Benefits: {', '.join(product['benefits'])}"))
        docs.append(("how_to_use", product["how_to_use"], f"How to use: {product['how_to_use']}"))
        docs.append(("side_effects", product["side_effects"], f"Side effects: {product['side_effects']}"))
        docs.append(("price_inr", str(product["price_inr"]), f"Price INR: {product['price_inr']}"))
        for q in items:
            qt = q["question"]
            selection_prompt = (
                "Choose the most relevant field to answer the question from the provided list. "
                "Return JSON with keys 'field' and 'answer'. Use only provided values.\n"
                f"Fields: {json.dumps([{f:v} for f, v, _ in docs], ensure_ascii=False)}\n"
                f"Question: {qt}"
            )
            text = llm.chat_json(selection_prompt)
            data = llm.ensure_json(text)
            field = data.get("field", docs[0][0])
            value = data.get("answer", "")
            answer_prompt = (
                "Answer the user's question using only the provided field and value. "
                "Keep the answer concise and grounded. If a yes/no is implied, answer directly. "
                "Do not invent facts.\n"
                f"Question: {qt}\n"
                f"Field: {field}\n"
                f"Value: {value}\n"
            )
            ans = llm.chat_json(answer_prompt).strip()
            faq_items.append({"q": qt, "a": ans, "category": q["category"], "source_field": field})

        return {
            "template": "faq",
            "product": product["product_name"],
            "supporting": {**ing, **usage, **safety},
            "qa": faq_items,
        }

    def build_product_page(self, product: Dict[str, Any]) -> Dict[str, Any]:
        spec = self.templates["product_page"]
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
        spec = self.templates["comparison_page"]
        comparison = self.logic_blocks["comparison_logic"](a, b)
        return {
            "template": "comparison_page",
            "product_a": a["product_name"],
            "product_b": b["product_name"],
            **comparison,
        }
