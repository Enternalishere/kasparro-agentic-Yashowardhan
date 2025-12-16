from typing import Dict, Any


class DocumentationAgent:
    def run(self, product_model: Dict[str, Any], questions: Dict[str, Any], logic_registry: Dict[str, Any], template_registry: Dict[str, Any]) -> str:
        return (
            "# Project Documentation\n\n"
            "## Problem Statement\n"
            "Transform a small structured product dataset into three machine-readable JSON pages using a modular multi-agent pipeline.\n\n"
            "## Solution Overview\n"
            "The system orchestrates seven focused agents that communicate strictly via JSON. Each agent has a single responsibility: parse input, generate questions, register logic blocks, define templates, create a comparable fictional product, assemble pages, and produce documentation.\n\n"
            "## Scope & Assumptions\n"
            "- Operates only on the provided product data type.\n"
            "- No external facts are introduced.\n"
            "- Outputs are JSON files plus this Markdown.\n\n"
            "## System Design\n"
            "- Data Flow: Raw→Parsing→Questions→Logic Blocks→Templates→Fictional Product→Assembly→Outputs→Docs.\n"
            "- JSON Contracts: Each agent outputs a well-structured JSON artifact consumed by the next.\n"
            "- Extensibility: New logic blocks and templates can be added without modifying other agents; pages are assembled declaratively from dependencies.\n"
            "- Isolation: Agents do not share state beyond explicit JSON payloads.\n"
        )