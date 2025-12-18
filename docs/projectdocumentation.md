# Project Documentation

## Problem Statement
Transform a small structured or unstructured product description into three machine-readable JSON pages using an agentic, LLM-powered pipeline.

## Solution Overview
The system uses LangGraph to orchestrate specialized agents. LLMs power question generation, competitor synthesis, semantic FAQ answering, and optional parsing from unstructured text. Outputs are FAQ, Product, and Comparison JSON plus this Markdown.

## Scope & Assumptions
- Operates only on Vitamin C serum-like product inputs without external facts.
- Requires `OPENAI_API_KEY` and optionally `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`.
- Produces deterministic JSON structures; text content is LLM-generated within constraints.

## System Design
- Orchestration: LangGraph state graph coordinates nodes for Parse→Questions→Logic→Templates→Competitor→Pages→Docs.
- LLM Usage: 
  - QuestionGenerationAgent: creates categorized user questions from product data.
  - FictionalProductAgent: synthesizes a realistic competitor product JSON.
  - PageAssemblyAgent: answers questions via embedding similarity over product fields and LLM grounding.
  - ProductParsingAgent: extracts ProductModel from unstructured text when needed.
- Data Exchange: Agents pass JSON artifacts through the graph state.
- Extensibility: New blocks/templates or answer sources can be registered without changing other components.
