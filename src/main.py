import json
from pathlib import Path
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.product_parsing_agent import ProductParsingAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.content_logic_block_agent import ContentLogicBlockAgent
from agents.template_engine_agent import TemplateEngineAgent
from agents.fictional_product_agent import FictionalProductAgent
from agents.page_assembly_agent import PageAssemblyAgent
from agents.documentation_agent import DocumentationAgent

RAW_PRODUCT_DATA = {
    "product_name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": ["Oily", "Combination"],
    "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
    "benefits": ["Brightening", "Fades dark spots"],
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price_inr": 699,
}


def ensure_dirs():
    Path("outputs").mkdir(parents=True, exist_ok=True)
    Path("docs").mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


class PipelineState(TypedDict):
    raw: Dict[str, Any]
    product_model: Dict[str, Any]
    questions: Dict[str, Any]
    logic_registry: Dict[str, Any]
    template_registry: Dict[str, Any]
    product_b: Dict[str, Any]
    faq_page: Dict[str, Any]
    product_page: Dict[str, Any]
    comparison_page: Dict[str, Any]
    documentation_md: str


def run_pipeline():
    ensure_dirs()
    graph = StateGraph(PipelineState)

    parsing_agent = ProductParsingAgent()
    question_agent = QuestionGenerationAgent()
    logic_agent = ContentLogicBlockAgent()
    template_agent = TemplateEngineAgent()
    fictional_agent = FictionalProductAgent()
    assembly_agent = PageAssemblyAgent(
        logic_blocks=logic_agent.run(), templates=template_agent.run()
    )
    docs_agent = DocumentationAgent()

    def node_parse(state: PipelineState) -> PipelineState:
        pm = parsing_agent.run(state["raw"])
        state["product_model"] = pm
        return state

    def node_questions(state: PipelineState) -> PipelineState:
        qs = question_agent.run(state["product_model"])
        state["questions"] = qs
        return state

    def node_logic(state: PipelineState) -> PipelineState:
        state["logic_registry"] = logic_agent.run()
        return state

    def node_templates(state: PipelineState) -> PipelineState:
        state["template_registry"] = template_agent.run()
        return state

    def node_competitor(state: PipelineState) -> PipelineState:
        pb = fictional_agent.run(base_schema=state["product_model"])
        state["product_b"] = pb
        return state

    def node_pages(state: PipelineState) -> PipelineState:
        faq = assembly_agent.build_faq_page(state["product_model"], state["questions"])
        prod = assembly_agent.build_product_page(state["product_model"])
        comp = assembly_agent.build_comparison_page(state["product_model"], state["product_b"])
        state["faq_page"] = faq
        state["product_page"] = prod
        state["comparison_page"] = comp
        return state

    def node_docs(state: PipelineState) -> PipelineState:
        md = docs_agent.run(
            product_model=state["product_model"],
            questions=state["questions"],
            logic_registry=state["logic_registry"],
            template_registry=state["template_registry"],
        )
        state["documentation_md"] = md
        return state

    graph.add_node("parse", node_parse)
    graph.add_node("questions", node_questions)
    graph.add_node("logic", node_logic)
    graph.add_node("templates", node_templates)
    graph.add_node("competitor", node_competitor)
    graph.add_node("pages", node_pages)
    graph.add_node("docs", node_docs)

    graph.add_edge("parse", "questions")
    graph.add_edge("questions", "logic")
    graph.add_edge("logic", "templates")
    graph.add_edge("templates", "competitor")
    graph.add_edge("competitor", "pages")
    graph.add_edge("pages", "docs")
    graph.add_edge("docs", END)

    app = graph.compile()
    initial: PipelineState = {
        "raw": RAW_PRODUCT_DATA,
        "product_model": {},
        "questions": {},
        "logic_registry": {},
        "template_registry": {},
        "product_b": {},
        "faq_page": {},
        "product_page": {},
        "comparison_page": {},
        "documentation_md": "",
    }
    final = app.invoke(initial)
    write_json(Path("outputs/faq.json"), final["faq_page"])
    write_json(Path("outputs/product_page.json"), final["product_page"])
    write_json(Path("outputs/comparison_page.json"), final["comparison_page"])
    Path("docs/projectdocumentation.md").write_text(final["documentation_md"], encoding="utf-8")
    return {
        "architecture": TemplateEngineAgent.architecture_overview(),
        "agent_definitions": TemplateEngineAgent.agent_definitions(),
        "logic_blocks": final["logic_registry"],
        "templates": final["template_registry"],
        "outputs": {
            "faq": final["faq_page"],
            "product_page": final["product_page"],
            "comparison_page": final["comparison_page"],
        },
        "documentation_path": "docs/projectdocumentation.md",
    }


if __name__ == "__main__":
    artifacts = run_pipeline()
    print(json.dumps({
        "generated_files": [
            "outputs/faq.json",
            "outputs/product_page.json",
            "outputs/comparison_page.json",
            "docs/projectdocumentation.md"
        ]
    }, ensure_ascii=False))
