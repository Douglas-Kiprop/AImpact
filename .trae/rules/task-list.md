# AImpact Super Agent: Project Task List

## Phase 0: Prerequisites & Initial Setup

- [x] **Google Cloud Project:**
    - [x] Create or select an existing Google Cloud Project.
    - [x] Ensure billing is enabled for the project.
- [x] **Vertex AI Agent Builder APIs:**
    - [x] Navigate to the Google Cloud Console.
    - [x] Enable the "Vertex AI Agent Builder API" for your project.
- [x] **`google-adk` Installation:**
    - [x] Install Python (if not already installed, preferably version 3.9+).
    - [x] Open your terminal or command prompt.
    - [x] Install `google-adk` using pip: `pip install google-adk`
- [x] **Google Cloud Authentication:**
    - [x] Install the Google Cloud CLI (`gcloud`).
    - [x] Authenticate with Google Cloud: `gcloud auth application-default login`
    - [x] Set your Google Cloud Project ID: `gcloud config set project YOUR_PROJECT_ID`

## Phase 1: Core ADK Agent & Initial Tooling

### 1.1. Project & Environment Setup
- [x] Navigate to Project Root: `C:\Users\doug\Trae Projects\AImpact\`
- [x] Create `agents` directory: `mkdir agents` (You've already done this)
- [x] Create `agents\tools` directory: `mkdir agents\tools` (You've already done this)
- [x] Initialize Python Virtual Environment: `python -m venv .venv` (You've already done this)
- [x] Activate Virtual Environment: `.venv\Scripts\activate` (You've already done this)
- [x] Install `google-adk` in .venv: `pip install google-adk` (You've already done this)
- [x] Create `.env` file in project root: `C:\Users\doug\Trae Projects\AImpact\.env` (You've already done this)
- [x] Install `python-dotenv`: `pip install python-dotenv`
- [x] Create `agents\__init__.py` (You've already done this)
- [x] Create `agents\tools\__init__.py` (You've already done this)

### 1.2. ADK Agent Definition (e.g., AImpactSuperAgent)
- [ ] Create main agent file (e.g., `marketing_agent.py` or `aimpact_super_agent.py`) in `C:\Users\doug\Trae Projects\AImpact\agents\`:
    - [ ] Define the primary agent class (e.g., `AImpactSuperAgent`) inheriting from `LlmAgent`.
    - [ ] Set agent name (e.g., "AImpactSuperAgent").
    - [ ] Configure model for Gemini (e.g., `gemini-1.5-flash-001`) via `VertexAi`.
    - [ ] Implement system instruction for marketing/business intelligence.
    - [ ] Include (commented out) settings for multi-agent coordination if this agent is an orchestrator.
- [ ] Document local testing commands (`adk web`, `adk run`) in the agent's Python file comments or a `README.md` in the `agents` directory.

### 1.3. `seo_keyword_generator` Tool Implementation
- [ ] Create `seo_keyword_generator.py` in `C:\Users\doug\Trae Projects\AImpact\agents\tools\`:
    - [ ] Define `SeoKeywordGeneratorInputs` Pydantic model (product, pain_points, goals, current_solutions, expertise_level).
    - [ ] Define `SeoKeywordGeneratorOutputs` Pydantic model (keywords: list[str]).
    - [ ] Implement `generate_seo_keywords` function:
        - [ ] Retrieve `N8N_SEO_WEBHOOK_URL` from environment variables (using `python-dotenv`).
        - [ ] Handle missing `N8N_SEO_WEBHOOK_URL`.
        - [ ] Construct JSON payload for n8n webhook.
        - [ ] Make POST request to n8n webhook using `requests` (install if not already: `pip install requests`).
        - [ ] Implement error handling for request exceptions and JSON decoding.
    - [ ] Create `seo_keyword_generator_tool` as an ADK `FunctionTool`.
- [ ] Add `seo_keyword_generator_tool` to the primary agent's tool list in its Python file (e.g., `agents/marketing_agent.py`).
- [ ] Set `N8N_SEO_WEBHOOK_URL` in `C:\Users\doug\Trae Projects\AImpact\.env` for testing.

### 1.4. Future Tools (Placeholders)
- [ ] Outline `GoogleTrendsScraper` tool structure in `C:\Users\doug\Trae Projects\AImpact\agents\tools\google_trends_scraper.py` (or a design document):
    - [ ] Define inputs (keywords, timeframe, geo).
    - [ ] Define outputs (trend_data).
- [ ] Outline `ColdEmailGenerator` tool structure in `C:\Users\doug\Trae Projects\AImpact\agents\tools\cold_email_generator.py` (or a design document):
    - [ ] Define inputs (prospect_name, company_name, value_proposition, call_to_action).
    - [ ] Define outputs (email_subject, email_body).

### 1.5. n8n Workflow (for `seo_keyword_generator`)
- [ ] Create n8n workflow for `seo_keyword_generator`.
- [ ] Configure Webhook Trigger:
    - [ ] Set method to POST.
    - [ ] Note down Production URL for `N8N_SEO_WEBHOOK_URL`.
    - [ ] Implement API Key authentication for the webhook.
- [ ] Configure Processing Steps (e.g., LLM node):
    - [ ] Construct prompt using webhook input data.
    - [ ] Configure LLM to output JSON with a "keywords" array.
- [ ] (Optional) Add custom code/data transformation nodes if needed.
- [ ] Configure "Respond to Webhook" node:
    - [ ] Ensure response body is `{"keywords": [...]}`.
    - [ ] Set status code to 200.
- [ ] Secure n8n webhook with API key and ensure ADK tool sends it.

## Phase 2: Backend (FastAPI) & Frontend (React)

### 2.1. FastAPI Backend
- [ ] Create backend directory: `C:\Users\doug\Trae Projects\AImpact\backend\`
- [ ] Initialize FastAPI project (`main.py` in `backend/`).
- [ ] Define `POST /api/v1/message` endpoint:
    - [ ] Define request body Pydantic model (message: str, session_id: str, optional agent_name: str, optional tool_inputs: dict).
    - [ ] Define response body Pydantic model (response: str, session_id: str).
- [ ] Implement ADK Integration:
    - [ ] Instantiate agents from the `agents` directory as needed (e.g., based on `agent_name` from request or a default agent).
    - [ ] Process incoming message using the selected agent.
    - [ ] Handle tool invocations and relay responses.
- [ ] Configure Environment Variables in `.env` (e.g., `GOOGLE_CLOUD_PROJECT_ID`, `VERTEX_AI_LOCATION`).
- [ ] Add comment for optional rate limiting (e.g., using `slowapi`).
- [ ] Create `requirements.txt` for backend dependencies (fastapi, uvicorn, google-adk, pydantic, requests, python-dotenv).

### 2.2. React Frontend (`ChatInterface` Component)
- [ ] Create frontend directory: `C:\Users\doug\Trae Projects\AImpact\frontend\`
- [ ] Initialize React project (e.g., using `create-react-app` or Vite) inside `frontend/`.
- [ ] Create `ChatInterface.js` component (`frontend/src/components/`).
- [ ] Implement Core UI features in `ChatInterface.js`.
- [ ] Implement Styling (black background, glassmorphism, etc.).
- [ ] Implement API Interaction with `backend/api/v1/message`.
- [ ] Configure Environment Variables for frontend (e.g., `REACT_APP_API_BASE_URL` or `VITE_API_BASE_URL` in `frontend/.env`).
- [ ] Set up `App.js` to include `ChatInterface`.

## Phase 3: Testing, Deployment & Extensibility

### 3.1. Testing Plan
- [ ] ADK Agent Testing:
    - [ ] Test agents locally using `adk web` and `adk run` (specifying agent file, e.g., `adk web -a agents/marketing_agent.py`).
    - [ ] Test tools directly with sample inputs.
- [ ] FastAPI Backend Testing.
- [ ] Frontend Testing.
- [ ] n8n Workflow Testing.
- [ ] End-to-End Testing.
- [ ] Error Handling Testing.

### 3.2. Deployment Strategy
- [ ] ADK Agent Deployment (Vertex AI Agent Engine).
- [ ] FastAPI Backend Deployment (Google Cloud Run).
- [ ] React Frontend Deployment (Vercel/Netlify).
- [ ] Configuration Management for deployed environments.

### 3.3. Extensibility & Documentation
- [ ] New Tooling Process Documentation.
- [ ] Project Documentation (`README.md` in project root and potentially `agents/README.md`).
- [ ] Code Comments.

### General Project Management
- [ ] Version Control (Git): Initialize repository, commit regularly.
- [ ] Dependency Management.
- [ ] Regular review and refactoring.


Step 2: Configure Frontend to Talk to Local Flask Backend

Once your frontend is running locally, you'll need to modify its code to send API requests to your local Flask backend. Your Flask backend is currently running on http://localhost:8080 and the endpoint for querying the agent is /query-agent.

I'll need to see how your frontend currently makes API calls to guide you on this. Could you please provide the relevant code snippet from your frontend that handles API requests? For example, if it's a React app, it might be in a component that makes a fetch or axios call.