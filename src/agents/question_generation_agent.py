from typing import Dict, Any, List


class QuestionGenerationAgent:
    """Generates >=15 categorized user questions answerable from product data only."""

    def run(self, product: Dict[str, Any]) -> Dict[str, Any]:
        name = product["product_name"]
        questions: List[Dict[str, Any]] = []

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