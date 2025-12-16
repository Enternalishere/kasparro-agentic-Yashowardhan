import json
from pathlib import Path

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


def run_pipeline():
    ensure_dirs()

    
    parsing_agent = ProductParsingAgent()
    product_model = parsing_agent.run(RAW_PRODUCT_DATA)

    question_agent = QuestionGenerationAgent()
    questions = question_agent.run(product_model)

    
    logic_agent = ContentLogicBlockAgent()
    logic_registry = logic_agent.run()

    
    template_agent = TemplateEngineAgent()
    template_registry = template_agent.run()

    
    fictional_agent = FictionalProductAgent()
    product_b = fictional_agent.run(base_schema=product_model)

    
    assembly_agent = PageAssemblyAgent(
        logic_blocks=logic_registry, templates=template_registry
    )
    faq_page = assembly_agent.build_faq_page(product_model, questions)
    product_page = assembly_agent.build_product_page(product_model)
    comparison_page = assembly_agent.build_comparison_page(product_model, product_b)

    
    write_json(Path("outputs/faq.json"), faq_page)
    write_json(Path("outputs/product_page.json"), product_page)
    write_json(Path("outputs/comparison_page.json"), comparison_page)

   
    docs_agent = DocumentationAgent()
    documentation_md = docs_agent.run(
        product_model=product_model,
        questions=questions,
        logic_registry=logic_registry,
        template_registry=template_registry,
    )
    Path("docs/projectdocumentation.md").write_text(documentation_md, encoding="utf-8")

    
    return {
        "architecture": TemplateEngineAgent.architecture_overview(),
        "agent_definitions": TemplateEngineAgent.agent_definitions(),
        "logic_blocks": logic_registry,
        "templates": template_registry,
        "outputs": {
            "faq": faq_page,
            "product_page": product_page,
            "comparison_page": comparison_page,
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