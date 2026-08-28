# 🤖 HR Enterprise Chatbot — AI Accelerator Bootcamp (6th Edition)

> Built during the **Decoding Data Science AI Accelerator Bootcamp** (Aug 28–30, 2026) — a hands-on RAG-powered chatbot that answers employee questions using real HR policy documents.

[![CPD Certified](https://img.shields.io/badge/CPD-Certified-22d3ee?style=flat-square)](https://decodingdatascience.com/bootcamp)
[![Made with OpenAI](https://img.shields.io/badge/LLM-OpenAI-8b5cf6?style=flat-square)](https://platform.openai.com)
[![RAG](https://img.shields.io/badge/Architecture-RAG-f5a623?style=flat-square)]()

---

## 📖 Overview

Employees often struggle to find HR policy information — details about leave, benefits, onboarding, and company rules are usually buried in long PDFs and internal portals.

**This project** is an AI-powered HR assistant that lets employees ask questions in plain English and get clear, accurate answers pulled directly from official HR policy documents — instead of digging through handbooks themselves.

Built as part of the CPE Framework taught in the bootcamp:
- **C — Clarity:** define the problem, user, and scope
- **P — Prototype:** build the RAG pipeline and working chatbot
- **E — Evidence:** test, refine, and ship a demo-ready app

---

## ✨ Features

- 💬 Natural-language Q&A over HR policy documents
- 📄 Retrieval-Augmented Generation (RAG) — answers are grounded in your actual documents, not just model memory
- 🔍 Semantic search over chunked, embedded policy content
- 🖥️ Simple web UI for employees to chat with the assistant
- ⚡ Fast, deployable, and easy to extend with new documents

---

## 🧰 Tech Stack

| Layer | Tool |
|---|---|
| LLM (response generation) | [OpenAI](https://platform.openai.com) |
| Embeddings | OpenAI Embeddings |
| RAG orchestration | [LlamaIndex](https://www.llamaindex.ai/) |
| Vector database | [Pinecone](https://www.pinecone.io/) |
| UI | [Gradio](https://www.gradio.app/) |
| Language | Python |

---

## 📁 Project Structure
