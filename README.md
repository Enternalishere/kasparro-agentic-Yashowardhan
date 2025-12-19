Multi-Agent Content Generation System

Run the pipeline using:

python src/main.py


This repository implements a production-grade multi-agent content generation system that transforms structured product data into machine-readable JSON content pages.

This is not a content-writing or UI project.
It is a systems engineering challenge focused on agent design, orchestration, validation, and execution integrity.

🎯 Problem Statement

Most AI-driven content systems rely on monolithic scripts or prompt-only pipelines that are:

Hard to extend

Difficult to audit

Prone to hidden hardcoding or fallback behavior

The goal of this project is to design a modular, agentic automation system that:

Operates via independent, single-responsibility agents

Communicates only through structured JSON

Produces validated, machine-readable outputs

Remains extensible, testable, and audit-proof

🧩 Solution Overview

This project implements a multi-agent pipeline where:

Each agent performs exactly one responsibility

Agents never share global state

All inter-agent communication is explicit and structured

Content generation is driven by reusable logic blocks

Pages are assembled via a custom template engine

The pipeline is orchestrated as a typed DAG

Generated Outputs

📄 FAQ Page

📄 Product Description Page

📄 Comparison Page (vs fictional product)

All outputs are pure JSON and suitable for downstream automation.

🏗️ System Architecture
🔁 Execution Flow
Raw Product Data
   ↓
Product Parsing Agent
   ↓
Question Generation Agent
   ↓
Content Logic Block Agent
   ↓
Template Engine Agent
   ↓
Fictional Product Agent
   ↓
Page Assembly Agent
   ↓
Validated JSON Outputs
   ↓
Documentation Agent


The pipeline is executed as a DAG, allowing independent agents to be parallelized where applicable.

🤖 Agent Responsibilities
1️⃣ Product Parsing Agent

Normalizes raw input into a strict ProductModel

Enforces schema validation

Performs no content generation

2️⃣ Question Generation Agent

Generates 15+ categorized user questions

Categories include usage, safety, pricing, comparison, etc.

All questions are derived dynamically at runtime

Questions are answerable using only provided product data

3️⃣ Content Logic Block Agent

Defines reusable, atomic logic blocks such as:

extract_benefits

usage_instructions

safety_notes

ingredient_summary

price_context

comparison_logic

Logic blocks are deterministic and testable

No logic blocks generate free-form content independently

4️⃣ Template Engine Agent

Defines structured templates, not text blobs

Each template declares:

Required fields

Logic block dependencies

Schema constraints

Enforces validation and dependency resolution

Fails loudly on invalid or incomplete assemblies

5️⃣ Fictional Product Agent

Generates a fictional but comparable Product B

Uses the same ProductModel schema

Introduces no hidden advantages or external assumptions

6️⃣ Page Assembly Agent

Applies validated templates and logic blocks

Produces final JSON pages

Performs no schema enforcement (handled upstream)

7️⃣ Documentation Agent

Generates documentation dynamically from:

Agent definitions

Execution flow

Templates and logic blocks

No static or hardcoded documentation content

🔒 Execution & Integrity Guarantees

This system enforces strict execution integrity:

❌ No hardcoded questions, FAQs, pages, or documentation

❌ No mock, wrapper, or fallback agents

❌ No deterministic placeholder outputs

❌ No silent degradation paths

All outputs are:

Generated dynamically by agent execution

Derived from runtime inputs

Validated against declared schemas

If any agent fails or required dependencies are unavailable, the pipeline fails loudly and produces no output artifacts.

🧪 Validation & Testing

The repository includes automated tests for:

Logic block correctness

Template schema enforcement

Question count and categorization constraints

End-to-end DAG execution

All final JSON artifacts are validated before being written to disk.

⚙️ Configuration & Orchestration

Model names, thresholds, and limits are centralized in configuration

Agents do not hardcode infrastructure or model choices

Pipeline state is typed and schema-validated

Execution is observable and debuggable via structured logging

📦 Outputs

The system produces the following artifacts:

faq.json

product_page.json

comparison_page.json

docs/projectdocumentation.md

Each artifact is:

Schema-validated

Machine-readable

Generated via agent orchestration (not static files)

🚫 What This Project Is NOT

❌ Not a UI or frontend project

❌ Not a monolithic script

❌ Not prompt-only content generation

❌ Not dependent on external data or assumptions

This project emphasizes system correctness over superficial generation
