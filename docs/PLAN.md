# Detailed Project Plan

## Part 1: Plan

**Objective:** Enrich the plan document with detailed substeps, checklists, tests, and success criteria for each subsequent part. Create AGENTS.md in frontend/ describing existing code. Obtain user approval.

**Substeps:**
- [ ] Review existing AGENTS.md (root) and docs/PLAN.md.
- [ ] Break down each of Parts 2-10 into detailed substeps with actionable checklists.
- [ ] Define tests (unit, integration, e2e) and success criteria for each part.
- [ ] Create frontend/AGENTS.md describing the existing frontend code structure, components, and functionality.
- [ ] Present the enriched plan to the user for review and approval.

**Tests:** Manual review and approval by user.

**Success Criteria:** Enriched docs/PLAN.md with all details, frontend/AGENTS.md created, user confirms approval.

## Part 2: Scaffolding

**Objective:** Set up Docker infrastructure, FastAPI backend, and start/stop scripts. Verify with a 'hello world' example serving static HTML and making an API call.

**Substeps:**
- [x] Create Dockerfile in project root for containerizing the app (NextJS frontend + FastAPI backend).
- [x] Set up backend/ directory with FastAPI app structure (main.py, requirements.txt or pyproject.toml for uv).
- [x] Implement a basic FastAPI route serving static HTML (e.g., "Hello World") at /.
- [x] Add a test API route (e.g., GET /api/test returning JSON).
- [x] Create scripts/start.sh and scripts/stop.sh for Mac, PC, Linux to build/run/stop the Docker container.
- [ ] Test locally: Run container, verify HTML served at /, API call works.

**Tests:**
- Unit: Test FastAPI routes with pytest.
- Integration: Docker build succeeds, container starts.
- E2e: Browser loads / and shows HTML, API endpoint returns expected JSON.

**Success Criteria:** Docker container runs locally, serves static HTML at /, API call returns data, start/stop scripts work on target platforms.

## Part 3: Add in Frontend

**Objective:** Integrate the existing frontend into the Docker setup, statically build and serve it at /, with comprehensive tests.

**Substeps:**
- [x] Update Dockerfile to build NextJS frontend statically.
- [x] Configure FastAPI to serve the built NextJS static files at /.
- [x] Ensure the Kanban board demo loads correctly in the container.
- [x] Run existing unit tests (Vitest) in container.
- [x] Run existing e2e tests (Playwright) against the containerized app.

**Tests:**
- Unit: All existing Vitest tests pass.
- Integration: NextJS build succeeds in Docker.
- E2e: All Playwright tests pass against containerized app.

**Success Criteria:** Container serves the Kanban demo at /, all tests pass, board is fully functional.

## Part 4: Add in a fake user sign in experience

**Objective:** Add login page requiring dummy credentials ("user", "password"), logout functionality, with comprehensive tests.

**Substeps:**
- [ ] Create login page component in frontend.
- [ ] Add authentication state management (hardcoded check).
- [ ] Protect Kanban board behind login; redirect to login if not authenticated.
- [ ] Add logout button/functionality.
- [ ] Update routing to handle login flow.
- [ ] Add unit tests for login logic.
- [ ] Add e2e tests for login/logout flow.

**Tests:**
- Unit: Authentication functions work correctly.
- Integration: Login state persists across page reloads.
- E2e: Login with correct creds shows board, incorrect denies, logout redirects to login.

**Success Criteria:** App requires login to access Kanban, logout works, all tests pass.

## Part 5: Database modeling

**Objective:** Propose and document database schema for Kanban data stored as JSON. Get user sign-off.

**Substeps:**
- [ ] Analyze frontend data structures (BoardData, Card, Column).
- [ ] Design SQLite schema/tables for users, boards, columns, cards.
- [ ] Document schema in docs/DATABASE.md, including JSON storage approach.
- [ ] Create sample database with initial data.
- [ ] Present to user for approval.

**Tests:** Manual review of schema design.

**Success Criteria:** docs/DATABASE.md created with schema, user approves design.

## Part 6: Backend

**Objective:** Add API routes for reading/changing Kanban data per user, with thorough backend unit tests. Database created if needed.

**Substeps:**
- [ ] Implement SQLite database setup in backend.
- [ ] Add API routes: GET /api/board/{user_id}, PUT /api/board/{user_id} for full board updates.
- [ ] Add routes for specific operations (add card, move card, etc.) if needed.
- [ ] Ensure database initializes with schema on first run.
- [ ] Write comprehensive unit tests for all routes and database operations.

**Tests:**
- Unit: All API routes tested with mocked DB, database CRUD operations tested.
- Integration: API calls work with real DB.

**Success Criteria:** Backend serves Kanban data via API, persists changes, all unit tests pass, DB created automatically.

## Part 7: Frontend + Backend

**Objective:** Connect frontend to backend API for persistent Kanban board, with thorough testing.

**Substeps:**
- [ ] Update frontend to fetch board data from API on load.
- [ ] Implement API calls for all board operations (add, move, delete, rename).
- [ ] Handle loading states and errors.
- [ ] Update authentication to tie to user ID.
- [ ] Run all existing tests against backend-connected app.
- [ ] Add integration tests for API interactions.

**Tests:**
- Unit: API client functions tested.
- Integration: Frontend-backend data flow works.
- E2e: Full user flows (login, manipulate board) work end-to-end.

**Success Criteria:** Board persists data via backend, all operations work, tests pass.

## Part 8: AI connectivity

**Objective:** Enable backend AI calls via OpenRouter, test with simple query.

**Substeps:**
- [ ] Set up OpenRouter client in backend using OPENROUTER_API_KEY.
- [ ] Add API route for AI test: POST /api/ai/test with simple prompt (e.g., "2+2").
- [ ] Verify response from openai/gpt-oss-120b model.
- [ ] Handle errors (API key, network).

**Tests:**
- Unit: AI client functions tested.
- Integration: Test route returns expected AI response.

**Success Criteria:** AI call works, test route responds correctly.

## Part 9: AI Kanban integration

**Objective:** Extend AI to process Kanban JSON + user questions, return structured outputs with optional board updates.

**Substeps:**
- [ ] Define structured output schema for AI (response text + optional board changes).
- [ ] Update AI route to accept board JSON, user question, conversation history.
- [ ] Parse AI response, apply board updates if present.
- [ ] Add conversation history management.
- [ ] Thoroughly test AI responses and board updates.

**Tests:**
- Unit: AI parsing and update logic tested.
- Integration: Full AI interaction with board changes.

**Success Criteria:** AI can update board based on queries, responses are structured, all tests pass.

## Part 10: AI chat UI

**Objective:** Add sidebar chat widget for AI interaction, auto-refresh UI on board updates.

**Substeps:**
- [ ] Design and implement chat sidebar component.
- [ ] Integrate with AI API, display conversation.
- [ ] Handle board updates from AI, trigger UI refresh.
- [ ] Add chat input, send messages.
- [ ] Style beautifully per color scheme.
- [ ] Test full chat flow.

**Tests:**
- Unit: Chat components tested.
- E2e: Complete chat interaction, board updates reflect in UI.

**Success Criteria:** Sidebar chat works, AI updates board and UI refreshes, all tests pass.