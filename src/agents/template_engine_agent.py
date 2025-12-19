from typing import Dict, Any, List
from models import TemplateSpec


class TemplateEngineAgent:
    """Defines structured templates with required fields, dependencies, and rules."""

    def run(self) -> Dict[str, Any]:
        specs: Dict[str, TemplateSpec] = {
            "faq": TemplateSpec(
                name="faq",
                required_fields=["product_name", "questions"],
                logic_dependencies=["ingredient_summary", "usage_instructions", "safety_notes"],
                format_rules={"qa_minimum": 15},
            ),
            "product_page": TemplateSpec(
                name="product_page",
                required_fields=[
                    "product_name",
                    "concentration",
                    "skin_type",
                    "key_ingredients",
                    "benefits",
                    "how_to_use",
                    "side_effects",
                    "price_inr",
                ],
                logic_dependencies=[
                    "extract_benefits",
                    "ingredient_summary",
                    "price_context",
                    "usage_instructions",
                    "safety_notes",
                ],
                format_rules={"schema_version": "1.0"},
            ),
            "comparison_page": TemplateSpec(
                name="comparison_page",
                required_fields=["product_a", "product_b"],
                logic_dependencies=["comparison_logic"],
                format_rules={"show_equals": True},
            ),
        }
        return {"templates": {k: v.model_dump() for k, v in specs.items()}}

    def enforce(self, template_registry: Dict[str, Any], name: str, payload: Dict[str, Any], logic_ids: List[str]) -> None:
        spec = template_registry["templates"][name]
        reqs = spec["required_fields"]
        deps = spec["logic_dependencies"]
        for rf in reqs:
            if rf == "questions":
                if "items" not in payload.get("questions", payload):
                    raise ValueError(f"Missing questions items for template {name}")
            elif rf == "product_a":
                if "product_name" not in payload.get("product_a", payload.get("a", {})):
                    raise ValueError("Missing product_a name")
            elif rf == "product_b":
                if "product_name" not in payload.get("product_b", payload.get("b", {})):
                    raise ValueError("Missing product_b name")
            else:
                if rf not in payload:
                    raise ValueError(f"Missing required field {rf} for template {name}")
        for dep in deps:
            if dep not in logic_ids:
                raise ValueError(f"Missing logic dependency {dep} for template {name}")

    @staticmethod
    def architecture_overview() -> Dict[str, Any]:
        return {
            "overview": {
                "flow": [
                    "Raw Product Data",
                    "Product Parsing Agent",
                    "Question Generation Agent",
                    "Content Logic Block Agent",
                    "Template Engine Agent",
                    "Fictional Product Agent",
                    "Page Assembly Agent",
                    "JSON Outputs",
                    "Documentation Agent",
                ],
                "communication": "Agents exchange structured JSON only; each has a single responsibility.",
                "extensibility": "New blocks and templates can be registered without changing agents.",
            }
        }

    @staticmethod
    def agent_definitions() -> Dict[str, Any]:
        return {
            "agents": [
                {"name": "Product Parsing Agent", "input": "Raw product JSON", "output": "ProductModel JSON"},
                {"name": "Question Generation Agent", "input": "ProductModel", "output": ">=15 questions grouped by category"},
                {"name": "Content Logic Block Agent", "input": "None", "output": "Registry of pure blocks"},
                {"name": "Template Engine Agent", "input": "None", "output": "Template registry (FAQ/Product/Comparison)"},
                {"name": "Fictional Product Agent", "input": "Base ProductModel schema", "output": "Product B (ProductModel)"},
                {"name": "Page Assembly Agent", "input": "Product(s), questions, logic, templates", "output": "faq.json, product_page.json, comparison_page.json"},
                {"name": "Documentation Agent", "input": "Artifacts", "output": "Markdown documentation"},
            ]
        }
