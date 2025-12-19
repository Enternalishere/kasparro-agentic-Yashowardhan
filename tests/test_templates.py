from agents.template_engine_agent import TemplateEngineAgent


def test_template_specs_required_fields():
    agent = TemplateEngineAgent()
    specs = agent.run()["templates"]
    faq = specs["faq"]
    assert "required_fields" in faq
    assert "logic_dependencies" in faq
    assert "format_rules" in faq
