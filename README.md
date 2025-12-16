# Multi-Agent Content Generation System


Run `python src/main.py` to generate JSON outputs and documentation.


A **production-grade agentic automation system** that transforms structured product data into **machine-readable content pages** using modular AI agents, reusable logic blocks, and a custom template engine.

This project demonstrates **Applied AI Engineering**, focusing on **system design, orchestration, abstraction, and extensibility** — not content writing or UI.

---

## 🎯 Problem Statement

Modern content systems often rely on monolithic pipelines that are difficult to scale, extend, or reason about.  
The goal of this project is to design a **modular multi-agent system** that:

- Understands structured product data
- Autonomously generates user-centric content
- Produces clean, machine-readable outputs
- Remains extensible to new products and templates

The system operates **entirely through cooperating agents**, each with a single responsibility and well-defined inputs/outputs.

---

## 🧩 Solution Overview

This project implements a **multi-agent content generation pipeline** where:

- Each agent performs **one focused task**
- Agents communicate only via **structured JSON**
- Content generation is driven by **reusable logic blocks**
- Output pages are assembled using a **custom template engine**
- The entire flow is orchestrated as a deterministic pipeline

The system produces:
- 📄 FAQ Page
- 📄 Product Description Page
- 📄 Comparison Page (against a fictional competitor)

All outputs are **valid JSON** and suitable for downstream automation.

---

## 🏗️ System Architecture

### 🔁 Execution Flow
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
JSON Content Pages
↓
Documentation Agent


---

## 🤖 Agent Responsibilities

### 1️⃣ Product Parsing Agent
- Normalizes raw input into a strict `ProductModel`
- Validates schema
- No content generation

### 2️⃣ Question Generation Agent
- Generates 15+ categorized user questions
- Categories include usage, safety, purchase, comparison, etc.
- Questions are answerable using product data only

### 3️⃣ Content Logic Block Agent
- Builds reusable, atomic transformation units
- Examples:
  - `extract_benefits`
  - `usage_instructions`
  - `safety_notes`
  - `ingredient_summary`
  - `price_context`
  - `comparison_logic`

### 4️⃣ Template Engine Agent
- Defines structured templates (not text blobs)
- Declares:
  - required fields
  - logic block dependencies
  - formatting rules

### 5️⃣ Fictional Product Agent
- Generates a comparable fictional Product B
- Uses the same schema
- No hidden advantages or external assumptions

### 6️⃣ Page Assembly Agent
- Applies templates + logic blocks
- Produces final JSON pages

### 7️⃣ Documentation Agent
- Generates system documentation
- Focuses on architecture and design decisions

---

## 🧠 Design Principles

- **Single Responsibility per Agent**
- **No hidden global state**
- **JSON-only communication**
- **Composable logic blocks**
- **Template-driven content**
- **Extensible to new products & pages**

---

## 📦 Outputs

The system generates the following machine-readable outputs:

- `faq.json`
- `product_page.json`
- `comparison_page.json`
- `docs/projectdocumentation.md`

Each output is:
- Deterministic
- Schema-consistent
- Ready for downstream consumption

---

## 🚫 What This Project Is NOT

- ❌ Not a UI or frontend project
- ❌ Not a monolithic script
- ❌ Not prompt-only content generation
- ❌ Not dependent on external data or research

This is a **systems engineering challenge**, not a copywriting task.

---

## 🧪 Extensibility

The architecture supports:
- New product types
- Additional templates
- New content logic blocks
- Alternate orchestration strategies (DAGs, state machines)

---

## 🏁 Conclusion

This project demonstrates how **agentic AI systems** can be designed with the same rigor as production software systems — emphasizing modularity, clarity, and correctness over ad-hoc generation.

It reflects the type of **automation-first, system-oriented AI engineering** used in real-world applied AI teams.

---






