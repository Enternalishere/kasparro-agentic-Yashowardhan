import json
from pathlib import Path
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from models import PipelineState, ProductModel, QuestionSet, FAQPage, ProductPage, ComparisonPage
from agents.product_parsing_agent import ProductParsingAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.content_logic_block_agent import ContentLogicBlockAgent
from agents.template_engine_agent import TemplateEngineAgent
from agents.fictional_product_agent import FictionalProductAgent
from agents.page_assembly_agent import PageAssemblyAgent
from agents.documentation_agent import DocumentationAgent
from validation_agent import FinalValidationAgent
from observability import agent_span
from local_llm import LocalLLMProvider, ConfigurationError

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


def run_pipeline():
    ensure_dirs()
    llm = LocalLLMProvider()
    llm.ping()
    graph = StateGraph(PipelineState)

    parsing_agent = ProductParsingAgent()
    question_agent = QuestionGenerationAgent()
    logic_agent = ContentLogicBlockAgent()
    template_agent = TemplateEngineAgent()
    fictional_agent = FictionalProductAgent()
    runtime_logic = logic_agent.get_impl()
    runtime_templates = template_agent.run()
    assembly_agent = PageAssemblyAgent(logic_blocks={"impl": runtime_logic}, templates=runtime_templates)
    docs_agent = DocumentationAgent()
    validator = FinalValidationAgent()

    def node_parse(state: PipelineState) -> PipelineState:
        with agent_span("ProductParsingAgent"):
            pm = parsing_agent.run(state["raw"])
        ProductModel.model_validate(pm)
        return PipelineState.model_validate({**state.model_dump(), "product_model": pm})

    def node_questions(state: PipelineState) -> PipelineState:
        with agent_span("QuestionGenerationAgent"):
            qs = question_agent.run(state["product_model"])
        QuestionSet.model_validate(qs)
        return PipelineState.model_validate({**state.model_dump(), "questions": qs})

    def node_logic(state: PipelineState) -> PipelineState:
        ids = logic_agent.block_ids()
        return PipelineState.model_validate({**state.model_dump(), "logic_ids": ids})

    def node_templates(state: PipelineState) -> PipelineState:
        specs = runtime_templates["templates"]
        return PipelineState.model_validate({**state.model_dump(), "template_specs": specs})

    def node_competitor(state: PipelineState) -> PipelineState:
        with agent_span("FictionalProductAgent"):
            pb = fictional_agent.run(base_schema=state["product_model"])
        ProductModel.model_validate(pb)
        return PipelineState.model_validate({**state.model_dump(), "product_b": pb})

    def node_template_enforce(state: PipelineState) -> PipelineState:
        with agent_span("TemplateEngineEnforce"):
            template_agent.enforce(runtime_templates, "faq", {"product_name": state["product_model"]["product_name"], "questions": state["questions"]}, state["logic_ids"])
            template_agent.enforce(runtime_templates, "product_page", state["product_model"], state["logic_ids"])
            template_agent.enforce(runtime_templates, "comparison_page", {"product_a": state["product_model"], "product_b": state["product_b"]}, state["logic_ids"])
        return state

    def node_pages(state: PipelineState) -> PipelineState:
        with agent_span("PageAssemblyAgent"):
            faq = assembly_agent.build_faq_page(state["product_model"], state["questions"])
            prod = assembly_agent.build_product_page(state["product_model"])
            comp = assembly_agent.build_comparison_page(state["product_model"], state["product_b"])
        return PipelineState.model_validate({**state.model_dump(), "faq_page": faq, "product_page": prod, "comparison_page": comp})

    def node_docs(state: PipelineState) -> PipelineState:
        with agent_span("DocumentationAgent"):
            md = docs_agent.run(
                product_model=state["product_model"],
                questions=state["questions"],
                logic_registry={"blocks": state["logic_ids"]},
                template_registry={"templates": state["template_specs"]},
            )
        return PipelineState.model_validate({**state.model_dump(), "documentation_md": md})

    def node_validate(state: PipelineState) -> PipelineState:
        with agent_span("FinalValidationAgent"):
            validator.run(
                {
                    "questions": state["questions"],
                    "faq_page": state["faq_page"],
                    "product_page": state["product_page"],
                    "comparison_page": state["comparison_page"],
                }
            )
        return state

    def node_error(state: PipelineState) -> PipelineState:
        return state

    graph.add_node("parse", node_parse)
    graph.add_node("questions", node_questions)
    graph.add_node("logic", node_logic)
    graph.add_node("templates", node_templates)
    graph.add_node("competitor", node_competitor)
    graph.add_node("template_enforce", node_template_enforce)
    graph.add_node("pages", node_pages)
    graph.add_node("docs", node_docs)
    graph.add_node("validate", node_validate)
    graph.add_node("error", node_error)

    graph.add_edge("parse", "questions")
    graph.add_edge("parse", "logic")
    graph.add_edge("parse", "templates")
    graph.add_edge("parse", "competitor")
    graph.add_edge("questions", "template_enforce")
    graph.add_edge("competitor", "template_enforce")
    graph.add_edge("logic", "template_enforce")
    graph.add_edge("templates", "template_enforce")
    graph.add_edge("template_enforce", "pages")
    graph.add_edge("pages", "docs")
    graph.add_edge("docs", "validate")
    graph.add_edge("validate", END)

    app = graph.compile()
    initial = PipelineState.model_validate({
        "raw": RAW_PRODUCT_DATA,
        "product_model": None,
        "questions": None,
        "logic_ids": [],
        "template_specs": {},
        "product_b": None,
        "faq_page": None,
        "product_page": None,
        "comparison_page": None,
        "documentation_md": None,
        "error": None,
    })
    final = app.invoke(initial)
    write_json(Path("outputs/faq.json"), final["faq_page"])
    write_json(Path("outputs/product_page.json"), final["product_page"])
    write_json(Path("outputs/comparison_page.json"), final["comparison_page"])
    Path("docs/projectdocumentation.md").write_text(final["documentation_md"], encoding="utf-8")
    return {
        "architecture": TemplateEngineAgent.architecture_overview(),
        "agent_definitions": TemplateEngineAgent.agent_definitions(),
        "logic_blocks": {"blocks": final["logic_ids"]},
        "templates": {"templates": final["template_specs"]},
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
