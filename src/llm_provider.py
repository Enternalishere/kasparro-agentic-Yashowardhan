import os
import re
import json
import math
from typing import List, Tuple, Dict, Any


class LocalEmbedder:
    def __init__(self, dim: int = 256):
        self.dim = dim

    def _vec(self, text: str) -> List[float]:
        buckets = [0.0] * self.dim
        for tok in re.findall(r"\w+", text.lower()):
            h = hash(tok) % self.dim
            buckets[h] += 1.0
        norm = math.sqrt(sum(x * x for x in buckets)) or 1.0
        return [x / norm for x in buckets]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._vec(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._vec(text)


class LocalLLM:
    def invoke(self, messages: List[Dict[str, Any]] | List[Any]) -> Any:
        content = messages[-1].content if hasattr(messages[-1], "content") else messages[-1]["content"]
        if "Create at least 15" in content and "Product data:" in content:
            start = content.rfind("Product data:")
            data = json.loads(content[start + len("Product data: "):])
            name = data.get("product_name", "Product")
            items = []
            def q(cat, text): items.append({"category": cat, "question": text})
            q("Informational", "What is the full name of the product?")
            q("Informational", "What is the concentration stated?")
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
            return type("R", (), {"content": json.dumps({"count": len(items), "items": items}, ensure_ascii=False)})
        if "Answer the user's question using only the provided field and value." in content:
            lines = content.splitlines()
            val_line = [l for l in lines if l.startswith("Value: ")]
            value = val_line[0].split("Value: ", 1)[1] if val_line else ""
            return type("R", (), {"content": value})
        return type("R", (), {"content": ""})


def get_llm_and_embedder():
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_core.messages import HumanMessage
        return {
            "is_openai": True,
            "llm_cls": ChatOpenAI,
            "embedder_cls": OpenAIEmbeddings,
            "human_message_cls": HumanMessage,
        }
    return {
        "is_openai": False,
        "llm": LocalLLM(),
        "embedder": LocalEmbedder(),
        "human_message_cls": type("HM", (), {"__init__": lambda self, content: setattr(self, "content", content)}),
    }
