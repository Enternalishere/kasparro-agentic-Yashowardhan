from typing import Dict, Any


class DocumentationAgent:
    def run(self, product_model: Dict[str, Any], questions: Dict[str, Any], logic_registry: Dict[str, Any], template_registry: Dict[str, Any]) -> str:
        name = product_model["product_name"]
        qcount = int(questions.get("count", len(questions.get("items", []))))
        blocks = logic_registry.get("blocks", [])
        templates = list(template_registry.get("templates", {}).keys())
        return (
            "# Project Documentation\n\n"
            "## Problem Statement\n"
            "Transform a product description into three machine-readable JSON pages using an agentic, LLM-powered pipeline.\n\n"
            "## Runtime Summary\n"
            f"- Product: {name}\n"
            f"- Questions generated: {qcount}\n"
            f"- Logic blocks available: {', '.join(blocks)}\n"
            f"- Templates registered: {', '.join(templates)}\n\n"
            "## Agent Orchestration\n"
            "- Parse → Questions, Logic, Templates, Competitor (parallel) → Pages → Docs → Validation\n"
            "- All artifacts are validated via Pydantic models; failures stop the pipeline.\n\n"
            "## Output Artifacts\n"
            "- faq.json: LLM-answered Q&A grounded in product data via embeddings.\n"
            "- product_page.json: Structured product schema plus logic-derived blocks.\n"
            "- comparison_page.json: Field-by-field comparison with equality markers.\n"
        )
