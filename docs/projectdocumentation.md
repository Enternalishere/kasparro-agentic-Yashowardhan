# Project Documentation

## Problem Statement
Transform a small structured product dataset into three machine-readable JSON pages using a modular multi-agent pipeline.

## Solution Overview
The system orchestrates seven focused agents that communicate strictly via JSON. Each agent has a single responsibility: parse input, generate questions, register logic blocks, define templates, create a comparable fictional product, assemble pages, and produce documentation.

## Scope & Assumptions
- Operates only on the provided product data type.
- No external facts are introduced.
- Outputs are JSON files plus this Markdown.

## System Design
- Data Flow: Raw→Parsing→Questions→Logic Blocks→Templates→Fictional Product→Assembly→Outputs→Docs.
- JSON Contracts: Each agent outputs a well-structured JSON artifact consumed by the next.
- Extensibility: New logic blocks and templates can be added without modifying other agents; pages are assembled declaratively from dependencies.
- Isolation: Agents do not share state beyond explicit JSON payloads.
