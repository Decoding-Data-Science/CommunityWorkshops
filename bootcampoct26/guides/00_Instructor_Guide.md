# CPD UK Bootcamp | DecoBot Leave Assistant (Gemini) | Instructor Guide

**Format:** 3 days x about 2 hours (6 hours total). One story, one company, one topic: **leave at Decoding Data Science (DDS)**, 100 employees, one office in Dubai.

```
Day 1  Control the AI          System prompt + clarity               (no files)
Day 2  Give it the policy      RAG, chunking, retrieval testing      (policy PDF)
Day 3  Give it data + tools    SQL, 3 tools, agent                   (policy PDF + database)
```

## What is in this folder

| File | Purpose |
|---|---|
| `notebooks/Day1_System_Prompt_and_Clarity.ipynb` | Day 1 Colab notebook |
| `notebooks/Day2_RAG_and_Chunking.ipynb` | Day 2 Colab notebook |
| `notebooks/Day3_SQL_Tools_and_Agent.ipynb` | Day 3 Colab notebook |
| `data/DDS_Leave_Policy_v2.pdf` | The existing leave policy (DDS-HR-POL-001 v2.0), unchanged. Upload on Days 2 and 3 |
| `data/dds_leave.db` | SQLite database: 100 employees, 273 leave requests. Upload on Day 3 |
| `slides/Day1_Control_the_AI.pptx`, `Day2_RAG_and_Chunking.pptx`, `Day3_SQL_Tools_and_Agent.pptx` | Slide decks (15, 15 and 17 slides) with speaker notes and click animations |
| `slides/CPD_UK_Gemini_3_Day_Slides.pptx` | 3-slide programme overview |
| `build_database.py` | Rebuilds the database from scratch (same data every time) |

## Before class (30 minutes, once)

1. **Run each notebook yourself** end to end with your own key. I tested everything that does not call Gemini (database, SQL, tools, chunking, agent loop with a scripted stand-in model). The Gemini calls themselves have not been run, so this rehearsal matters.
2. **Model names.** Each notebook has one line `MODEL = "gemini-3.8-flash"` and Days 2 and 3 have `EMBED_MODEL = "gemini-embedding-001"`. These came from Google's model page and LlamaIndex's docs as of today. If either fails, change that single line.
3. **Participant setup (send 2 days before):** a Google account, a Gemini API key from Google AI Studio (with billing if free-tier limits are too tight for a live class), and the instruction to store it in Colab **Secrets** under the name `GOOGLE_API_KEY` with notebook access switched on.
4. Send the files each day (Day 2: PDF; Day 3: PDF + `.db`).

## Day 1 | System prompt and clarity (about 2 hours)

| Time | Part | What happens | Key moment |
|---|---|---|---|
| 0:00 | Intro | Story, 3-day map, plan | DDS has 100 people, HR answers the same questions weekly |
| 0:10 | Part 0 | Setup, Colab secret, first call | Everyone gets a reply from Gemini |
| 0:20 | Part A | Raw model, no prompt | Confident, generic, wrong for DDS (policy says 22 days, carry-over 10) |
| 0:30 | Part B | Prompt v1, v2, v3, scope tests | Same question, three behaviours; refusals for salary, medical, "ignore your instructions" |
| 1:00 | Part C | Clarity lab | Rule that makes the bot ask one clarifying question; remove it and compare |
| 1:15 | Part D | Cheat sheet in the prompt | Works for 6 facts; the sick-certificate question exposes the limit |
| 1:30 | Part E | JSON extraction | Text in, data out; bridge to tools |
| 1:40 | Part F | Prompt Clinic | Participants improve the prompt against 5 tests |

If you are short on time, drop Part E and shorten Part F to a take-home.

## Day 2 | RAG and chunking (about 2 hours)

| Time | Part | What happens | Key moment |
|---|---|---|---|
| 0:00 | Recap + Part 0 | Day 1 to RAG in 4 steps; setup, upload PDF, models | Diagram in the notebook |
| 0:15 | Part A | Embeddings | "vacation days" matches "annual leave" with no shared words |
| 0:25 | Part B | Load PDF, default index, show sources | Wrong answer? Read the retrieved chunks first |
| 0:40 | Part C | **Chunking lab** (the core of the day, 45 min) | Three strategies (4 / 28 / 13 chunks), the notice table (section 3.4) cut differently, scored mini test, top_k |
| 1:25 | Part D | Final engine, scenario cards, 2 trap questions | "Dress code" must say not found; "my balance" cannot be answered from a PDF |
| 1:45 | Wrap-up | Chunking checklist, tomorrow | |

**Be ready for different results.** The mini test scores the three strategies on 8 questions. Embedding models do not behave identically for everyone, so the winner may differ from what I expect (I expect section-based chunks to do well because the policy has numbered sections, but I could not run the real embeddings). Treat a surprise as a teaching moment: "measure, do not guess."

## Day 3 | SQL, tools and agent (about 2 hours)

| Time | Part | What happens | Key moment |
|---|---|---|---|
| 0:00 | Recap + Part 0 | Rules (Day 2) versus personal data (today); setup, upload PDF and database | Architecture diagram |
| 0:15 | Part A | SQL: SELECT/WHERE, ORDER BY, GROUP BY, JOIN, `?` parameters, 3 exercises (25 min) | Never glue user text into SQL |
| 0:40 | Part B | Three tools (balance, requests, policy search) | The docstring tells the agent when to use each tool |
| 1:00 | Part C | Build the agent, system prompt, `chat()` helper | Tool calls are printed live |
| 1:15 | Part D | Scenes 1 to 5 | Scene 3 uses both tools; Scene 5 refusals |
| 1:40 | Part E | Bad tool descriptions | Docstring is the routing logic |
| 1:50 | Wrap-up | Chatbot vs agent, where to go next | Optional free chat and the fourth-tool challenge as homework |

### The demo cast (all in the database)

| Employee | ID | Annual used / booked / left | Why useful |
|---|---|---|---|
| Aisha Khan | 1024 | 15 / 5 / **2** | Scene 3: asks for 5 days from 14 December. Notice is fine (14 required, 47 days away) but balance is not (2 left). Then the carry-over question |
| John Doe | 1025 | 5 / 0 / **17** | 10 days from 7 December: enough balance, 30 calendar days notice applies, date arithmetic |
| Maria Garcia | 1026 | 15 / 0 / 7 | Used for the "show me someone else's balance" refusal; also has a Study leave record |
| David Lee | 1027 | 5 / 0 / 17 | Joined November 2025, so under 2 years of service (study leave rule); has one Rejected request (28 to 31 December) for a "what happened to my request?" question |

Any name in the database works for live questions. A few first names repeat (for example several "Aisha"), so the tool asks the user to pick when a name is ambiguous. That is intentional and worth showing.

### Things to say out loud on Day 3
- The agent refuses to share other people's data **because the prompt says so**. A prompt is not security; production needs real authentication.
- All tools are **read-only** on purpose. An agent that can write is an agent that can do damage.
- Today's date is fixed at 2026-10-28 in the system prompt, so the notice-period arithmetic is reproducible.

### Policy quirk to know
Section 1 of the policy points to "section 4.4" for extended illness, but that content is in **section 5.4**. The materials do not hide it; if a participant notices, it is a nice example of why bots must quote sections.

## Slide decks (new)

Three decks in `slides/`, one per day, with word-for-word speaker notes. Each block on a slide fades in on click (OPEN / CLICK 1, 2, ... / CLOSE in the notes match the clicks). The animations only play in PowerPoint slideshow mode (not in preview or LibreOffice): do a quick run-through before class. `CPD_UK_Gemini_3_Day_Slides.pptx` is the 3-slide programme overview.

## Colab secret (every notebook)

Key icon on the left of Colab > Add new secret > name `GOOGLE_API_KEY`, value = your Gemini key > switch on Notebook access. The first code cell reads it with `userdata.get` and shows a clear message if it is missing. Never paste the key into a cell.

## Known limits of the materials (so nothing surprises you in class)

- The policy does not define the **probation period**, although sick leave starts after it. DecoBot will say it cannot find it. This is a useful honest-failure demo, but you can also pre-empt it.
- The database counts **working days as Monday to Friday** and does not subtract public holidays.
- Leave balances are computed from the requests table: Approved requests with a start date up to 2026-10-28 are "taken"; Approved later ones are "booked"; Pending, Rejected and Cancelled do not count.
- Free-tier Gemini limits can slow the Day 2 test (about 24 embedding calls per strategy run) in a large class.

## To take it further (beyond the 6 hours)

1. **Real identity:** the tool receives a verified employee ID from a login instead of a typed name.
2. **Write tools with confirmation:** `submit_leave_request`, always confirmed by the employee and routed to the manager.
3. **Evaluation set:** 50 to 100 questions with expected answers, rerun after every change (Day 2's mini test is the seed of this).
4. **More documents:** manager guide, FAQ, holiday calendar, and old policy versions handled with metadata so superseded rules are not retrieved.
5. **Logging:** record tool calls and every "not found" so HR can improve the policy.
6. **Deployment:** chat interface plus hosting (deliberately not covered in the bootcamp).
