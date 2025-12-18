from typing import Dict, Any, List
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class QuestionGenerationAgent:
    """Generates >=15 categorized user questions answerable from product data only."""

    def run(self, product: Dict[str, Any]) -> Dict[str, Any]:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        llm = ChatOpenAI(model=model_name, temperature=0)
        name = product["product_name"]
        prompt = (
            "You are a product Q&A generator. Create at least 15 concise, user-centric questions "
            "about the product, grouped into categories: Informational, Usage, Safety, Purchase, Ingredients, Comparison. "
            "Only use the provided product data. Return strict JSON with keys 'count' and 'items', where 'items' is a list "
            "of objects containing 'category' and 'question'. Do not add explanations.\n"
            f"Product data: {json.dumps(product, ensure_ascii=False)}"
        )
        msg = HumanMessage(content=prompt)
        res = llm.invoke([msg])
        text = res.content
        try:
            data = json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}") + 1
            data = json.loads(text[start:end])
        if "items" not in data or not isinstance(data["items"], list):
            raise ValueError("LLM did not return valid items list")
        return {"count": len(data["items"]), "items": data["items"]}

        def q(category: str, text: str):
            questions.append({"category": category, "question": text})

        
        q("Informational", f"What is the full name of the product?")
        q("Informational", f"What is the concentration stated?")
        q("Informational", f"Which skin types is {name} suitable for?")
        q("Informational", f"What are the key ingredients in {name}?")
        q("Informational", f"What benefits does {name} claim?")

        q("Usage", "How should I apply the product?")
        q("Usage", "When during the day should it be used?")
        q("Usage", "How many drops are recommended per application?")

        
        q("Safety", "Are there any noted side effects?")
        q("Safety", "Is tingling expected for sensitive skin?")

       
        q("Purchase", "What is the price in INR?")
        q("Purchase", "Does the product list include Vitamin C?")

       
        q("Ingredients", "Does it contain Hyaluronic Acid?")
        q("Ingredients", "How many key ingredients are listed?")

       
        q("Comparison", "Is the concentration explicitly 10% Vitamin C?")
        q("Comparison", "Are benefits focused on brightening and fading dark spots?")

        return {"count": len(questions), "items": questions}
