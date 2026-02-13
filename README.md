# Antigravity: Autonomous Digital Asset Ecosystem

**Version**: 2.0 (Production Ready)
**Architecture**: Async Event-Driven Python w/ React Frontend Support

## 🚀 Quick Start (Production Mode)

1.  **Clone & Install**:
    ```bash
    git clone ...
    pip install -r requirements.txt
    ```

2.  **Environment Setup**:
    Copy `.env.example` to `.env` and fill in:
    ```bash
    cp .env.example .env
    ```

    *   **MANDATORY**: `OPENAI_API_KEY`, `SERPER_API_KEY`
    *   **OPTIONAL**: `GITHUB_PERSONAL_ACCESS_TOKEN` (for publishing), `LEMONSQUEEZY_API_KEY` (for payments)
        *   *Note*: GitHub Token requires `repo` and `workflow` scopes.

3.  **Run**:
    ```bash
    python main.py
    ```

## 🛡️ Safety & QA Gates

The system now implements strict gates to ensure quality and safety:

*   **Feature Flags**: Enable/disable components via `.env` (e.g., `ENABLE_PUBLISH_GITHUB=false` for safe testing).
*   **Fail-Fast QA**:
    *   **Backend**: Python syntax check (`compileall`) + Flake8 linting.
    *   **Frontend**: `npm install` + `npm run build` (if `package.json` exists).
    *   *If any check fails, the pipeline ABORTS immediately before publishing.*

## 🧩 Architecture

*   **Scanner**: Monitors RSS/APIs for trends (HackerNews, TechCrunch, etc.).
*   **Analyzer**: Scores trends using LLM to find profitable opportunities.
*   **Generator**: Creates product concepts and tech specs.
*   **Builder**: Writes code (Python/React) based on the plan.
*   **Validator**: Verifies demand via Serper (Google Search).
*   **Publisher**: Pushes to GitHub and drafts Store products (LemonSqueezy).
