from agents.content_logic_block_agent import ContentLogicBlockAgent


def test_logic_block_ids_nonempty():
    agent = ContentLogicBlockAgent()
    ids = agent.block_ids()
    assert "ingredient_summary" in ids
    assert "extract_benefits" in ids
