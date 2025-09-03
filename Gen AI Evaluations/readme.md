# LLM & RAG Evaluation 

A lightweight starting point to **evaluate LLM/RAG systems**. Includes quick setup, notebooks, and the four core metrics used in most RAG projects.

---

## What’s inside
- `1-rag_evaluation.ipynb` — end-to-end RAG evaluation walkthrough  
- `1-rag_evaluation_recipe.ipynb` — short, reusable recipe for common evals  
- `requirements.txt` — Python dependencies for running the notebooks

---

## Quick start
```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Update environment variables with open ai key and langsmith key


# 4) Launch Jupyter and open a notebook
jupyter lab   # or: jupyter notebook


