# CPD UK Bootcamp | DecoBot Leave Assistant (Gemini)

A 3-day, about 6-hour programme built on one story: a leave-policy chatbot for Decoding Data Science (100 employees, Dubai).

| Day | Topic | Notebook | Slides | Files to upload in Colab |
|---|---|---|---|---|
| 1 | System prompt and clarity | notebooks/Day1_System_Prompt_and_Clarity.ipynb | slides/Day1_Control_the_AI.pptx | none |
| 2 | RAG with LlamaIndex, chunking lab | notebooks/Day2_RAG_and_Chunking.ipynb | slides/Day2_RAG_and_Chunking.pptx | data/DDS_Leave_Policy_v2.pdf |
| 3 | SQL, three tools, agent | notebooks/Day3_SQL_Tools_and_Agent.ipynb | slides/Day3_SQL_Tools_and_Agent.pptx | data/DDS_Leave_Policy_v2.pdf, data/dds_leave.db |

Start with `00_Instructor_Guide.md`.

## Quick start
1. Get a Gemini API key from Google AI Studio.
2. In Colab: key icon (Secrets) > add `GOOGLE_API_KEY` > switch on Notebook access.
3. Open the day's notebook (File > Upload notebook), upload the files from the table, run top to bottom.

Models are set in one line per notebook (`MODEL`, `EMBED_MODEL`). Change them there if Google renames a model.

## Other files
- `build_database.py`: rebuilds `data/dds_leave.db` (same data every time).
- `slides/CPD_UK_Gemini_3_Day_Slides.pptx`: 3-slide overview. Slide animations play in PowerPoint slideshow mode.
