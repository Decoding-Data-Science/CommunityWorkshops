# CPD UK AI Accelerator Bootcamp | DecoBot HR Leave Assistant (Gemini)

A 3-day, about 6-hour program on one story: a leave-policy chatbot for Decoding Data Science (100 employees, Dubai).
Tools: Google Colab, Gemini, LlamaIndex, Pinecone. Deploy: Hugging Face Spaces (Render optional).

| Folder | Contents |
|---|---|
| `index.html` | DecoBot RAG Lab: interactive page (chunking, retrieval, embeddings, agent, cost, data dictionary, glossary) |
| `notebooks/` | Day 1, Day 2 (memory), Day 2B (Pinecone), Day 3 Colab notebooks |
| `slides/` | PowerPoint decks with click animations (Day 1, 2, 3, overview, data understanding) |
| `slides_pdf/` | The same decks as PDF (animations are not in PDF) |
| `data/` | `DDS_Leave_Policy_v2.pdf`, `dds_leave.db`, `build_database.py` |
| `guides/` | Instructor guide and program README |

| Day | Notebook | Upload in Colab |
|---|---|---|
| 1 | Day1_System_Prompt_and_Clarity | none |
| 2 | Day2_RAG_and_Chunking, then Day2B_RAG_with_Pinecone | DDS_Leave_Policy_v2.pdf |
| 3 | Day3_SQL_Tools_and_Agent | DDS_Leave_Policy_v2.pdf and dds_leave.db |

Colab Secrets: `GOOGLE_API_KEY` (all days), `PINECONE_API_KEY` (Day 2B). Never commit a key.
All data is synthetic, for training.
