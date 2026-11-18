# Service Delivery Reporter (Community Voice)

Citizens report local service problems (water, electricity, roads, sanitation, waste) by text, voice note and an optional photo, in English, isiZulu, isiXhosa, Afrikaans or Sesotho. AI agents triage the report, check the web for known outages, route it to a department, flag duplicates and draft a reply. Citizens sign in to submit and follow their own reports. An admin reviews: the report, then the reply. Nothing is ever sent.

All sample data is fictional. This is a teaching project, not a production system.


## Set up

1. Install uv.

   Windows (run once in PowerShell):

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

 

2. From the project folder, install Python and the libraries:

   ```bash
   uv python install 3.12
   uv sync
   ```

3. Create your key file and fill it in. `.env` is git-ignored; never commit it.

   ```bash
   cp .env.example .env
   ```

   | Variable | Service | Where to get it |
   |---|---|---|
   | `GEMINI_API_KEY` | Triage, drafting, voice transcription | aistudio.google.com (API keys) |
   | `GROQ_API_KEY` | Routing, web check | console.groq.com/keys |
   | `TAVILY_API_KEY` | Web search | app.tavily.com |
   | `LANGSMITH_API_KEY` | Tracing and evals (optional) | smith.langchain.com, Settings, API Keys |
   | `JWT_SECRET` | Signs login tokens | Generate your own: `openssl rand -hex 32` |

   To trace runs in LangSmith, also add these two lines to `.env`. Tracing sends report text to LangSmith's cloud, so use fictional data only.

   ```
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=community-voice
   ```

4. Create the test accounts (see "Sign in" below):

   ```bash
   uv run python -m community_voice.auth.seed
   ```

5. Check the setup (no keys or network needed):

   ```bash
   uv run pytest
   ```

## Sign in

The API needs a login. The seed command above creates three **test accounts**. Their passwords are public: use them for demos only.

| Role | Email | Password |
|---|---|---|
| Admin (reviews reports and drafts, sees the dashboard) | `admin@communityvoice.test` | `AdminPass123` |
| Citizen 1 (submits reports, sees only their own) | `citizen1@communityvoice.test` | `Citizen1Pass123` |
| Citizen 2 (submits reports, sees only their own) | `citizen2@communityvoice.test` | `Citizen2Pass123` |

In the Streamlit app, sign in on the first screen. A citizen follows their reports and reads the reply on the My Reports page. The pages are the same for everyone, and the API refuses what the account may not do (a citizen opening the review queue gets "Admins only"). In the API docs page, use the Authorize button.

## Run the app

Open two terminals in the project folder and leave both running.

```bash
uv run uvicorn community_voice.api.main:app --port 8800
```

```bash
uv run streamlit run app/streamlit_app.py
```

Streamlit opens at http://localhost:8501. The API's interactive docs are at http://127.0.0.1:8800/docs. Stop each with Ctrl+C. To start with a clean slate, delete `data/app.db`.

### Next.js app (the full interface)

The Next.js app has both roles: citizens submit reports and follow them; the admin reviews. Install and run it once with the API running:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open http://localhost:3000 and sign in with a test account above 

## Other things to run

- Notebooks: open `notebooks/` in VS Code and pick the project's `.venv` as the kernel. Clear the outputs before committing.
- Evals (scores triage and routing on 20 labelled reports):

  ```bash
  uv run python -m evals.run_evals --refresh
  ```



