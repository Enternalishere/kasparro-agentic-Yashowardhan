from typing import Dict, Any


class TemplateEngineAgent:
    """Defines structured templates with required fields, dependencies, and rules."""

    def run(self) -> Dict[str, Any]:
        return {
            "templates": {
                "faq": {
                    "required_fields": ["product_name", "questions"],
                    "logic_dependencies": ["ingredient_summary", "usage_instructions", "safety_notes"],
                    "format_rules": {"qa_minimum": 5},
                },
                "product_page": {
                    "required_fields": [
                        "product_name",
                        "concentration",
                        "skin_type",
                        "key_ingredients",
                        "benefits",
                        "how_to_use",
                        "side_effects",
                        "price_inr",
                    ],
                    "logic_dependencies": [
                        "extract_benefits",
                        "ingredient_summary",
                        "price_context",
                        "usage_instructions",
                        "safety_notes",
                    ],
                    "format_rules": {"schema_version": "1.0"},
                },
                "comparison_page": {
                    "required_fields": ["product_a", "product_b"],
                    "logic_dependencies": ["comparison_logic"],
                    "format_rules": {"show_equals": True},
                },
            }
        }

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