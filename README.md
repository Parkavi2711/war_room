# AI Product Launch War Room — Multi-Agent Decision System

A multi-agent AI system that simulates a cross-functional **war room** during a product launch. The system analyzes product metrics, user feedback, and known issues to produce a structured launch decision — **Proceed**, **Pause**, or **Roll Back** — along with rationale from each agent and a confidence score.

---

## Table of Contents

- [Problem Overview](#problem-overview)
- [Architecture](#architecture)
- [Agents](#agents)
- [Tools](#tools)
- [Data Inputs](#data-inputs)
- [LLM Usage](#llm-usage)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Output Format](#output-format)
- [Tech Stack](#tech-stack)

---

## Problem Overview

During a product launch, multiple signals change simultaneously — some positive, others indicating risk. This project simulates how different cross-functional teams collaborate to make a data-driven rollout decision.

**Key objectives:**

- Multi-agent orchestration with clearly defined roles
- Deterministic tool-based quantitative analysis
- LLM-powered qualitative reasoning
- Transparent and traceable decision-making pipeline

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                     main.py                         │
│              (Orchestration Entry Point)            │
└────────┬──────────────┬──────────────┬──────────────┘
         │              │              │
         ▼              ▼              ▼
┌────────────┐  ┌──────────────┐  ┌────────────┐
│   Data     │  │  Marketing   │  │   Risk     │
│  Analyst   │  │    Agent     │  │   Agent    │
│   Agent    │  │              │  │  (Critic)  │
└─────┬──────┘  └──────┬───────┘  └─────┬──────┘
      │                │                │
      │  ┌─────────────┘                │
      │  │  ┌───────────────────────────┘
      ▼  ▼  ▼
┌─────────────────┐
│   Coordinator   │──────▶  Final Decision (JSON)
│     Agent       │
└─────────────────┘
```

Each agent uses **deterministic tools** for data processing and an **LLM** (Gemma 2B via Ollama) for reasoning. The Coordinator synthesizes all outputs using consensus logic.

---

## Agents

| Agent | File | Role |
|---|---|---|
| **Data Analyst** | `agents/data_analyst_agent.py` | Analyzes quantitative metrics (trends, anomalies) from `metrics.csv`. Uses `metrics_tools` for computation and the LLM for health assessment. |
| **Marketing / Comms** | `agents/marketing_agent.py` | Evaluates user sentiment and perception risk from `feedback.json`. Uses `feedback_tools` for classification and the LLM for messaging strategy. |
| **Risk / Critic** | `agents/risk_agent.py` | Challenges assumptions from other agents, highlights worst-case risks, and reviews `release_notes.md`. Uses the LLM for critical reasoning. |
| **Coordinator** | `agents/coordinator.py` | Synthesizes all agent outputs into a final decision using consensus logic: any "Roll Back" → Roll Back; ≥2 "Pause" → Pause; otherwise → Proceed. |

---

## Tools

Deterministic Python tools handle all numerical and data processing (no LLM involved):

### `tools/metrics_tools.py`

| Function | Description |
|---|---|
| `load_metrics(csv_path)` | Loads metrics CSV into a pandas DataFrame |
| `analyze_trends(df)` | Compares first vs. last values for each metric; classifies as `increasing`, `decreasing`, or `stable` (±5% threshold) |
| `detect_anomalies(df)` | Flags anomalies on the latest row using fixed thresholds — crash rate > 1.5%, API latency p95 > 280 ms, support tickets > 40 |

### `tools/feedback_tools.py`

| Function | Description |
|---|---|
| `load_feedback(json_path)` | Loads user feedback entries from a JSON file |
| `analyze_feedback(entries)` | Classifies each entry as positive, neutral, or negative using keyword matching; returns sentiment distribution and top recurring issues |

---

## Data Inputs

The system consumes three data files from the `data/` directory:

| File | Format | Description |
|---|---|---|
| `metrics.csv` | CSV | 10 days of product metrics — `activation_rate`, `dau`, `d1_retention`, `crash_rate`, `api_latency_p95_ms`, `support_tickets` |
| `feedback.json` | JSON | 20 user feedback entries with `user_id` and `feedback` text |
| `release_notes.md` | Markdown | Feature summary, known issues, and rollout status for the current release |

---

## LLM Usage

| Property | Value |
|---|---|
| **Model** | Gemma 1B |
| **Runtime** | Ollama (local execution) |
| **API Keys** | Not required |
| **Endpoint** | `http://localhost:11434` |

The LLM is used **only for agent reasoning** — interpreting trends, assessing sentiment risk, and challenging assumptions. All quantitative analysis is performed by deterministic Python tools, ensuring reproducibility and transparency.

The LLM client is implemented in `llm/ollama_client.py`.

---

## Project Structure

```
war_room_llm/
│
├── agents/                        # Agent definitions
│   ├── coordinator.py             # Synthesizes final decision via consensus logic
│   ├── data_analyst_agent.py      # Metrics analysis + LLM reasoning
│   ├── marketing_agent.py         # Feedback analysis + LLM reasoning
│   └── risk_agent.py              # Risk assessment + LLM critical reasoning
│
├── tools/                         # Deterministic analysis tools
│   ├── metrics_tools.py           # Trend analysis and anomaly detection
│   └── feedback_tools.py          # Sentiment classification and issue extraction
│
├── llm/                           # LLM integration
│   └── ollama_client.py           # Ollama API client for Gemma 2B
│
├── data/                          # Input data files
│   ├── metrics.csv                # Product metrics (10-day time series)
│   ├── feedback.json              # User feedback entries
│   └── release_notes.md           # Release notes and known issues
│
├── logs/                          # Runtime logs (output directory)
├── output/                        # Generated output files
│
├── main.py                        # CLI entry point — runs all agents
├── ui.py                          # Streamlit web UI
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
# Create
python -m venv pm_env

# Activate (Windows)
pm_env\Scripts\activate

# Activate (Linux / macOS)
source pm_env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Ollama

1. Install Ollama from [https://ollama.com](https://ollama.com)
2. Pull the Gemma 2B model:

```bash
ollama run gemma3:1b
```

Ollama runs locally at `http://localhost:11434` — no API keys required.

---

## How to Run

### CLI Mode

```bash
python main.py
```

Runs all agents, performs analysis, and prints the final structured decision as JSON to the console.

### Streamlit UI

```bash
streamlit run ui.py
```

Provides a web-based interface with a **Run War Room Simulation** button. Displays the final decision and full agent rationale in the browser.

---

## Output Format

The system produces a structured JSON response:

```json
{
  "decision": "Proceed | Pause | Roll Back",
  "rationale": [
    {
      "agent": "DataAnalyst",
      "analysis": "LLM reasoning output..."
    },
    {
      "agent": "Marketing",
      "analysis": "LLM reasoning output..."
    },
    {
      "agent": "RiskCritic",
      "analysis": "LLM reasoning output..."
    }
  ],
  "confidence_score": 0.67
}
```

### Decision Logic (Coordinator)

| Condition | Decision |
|---|---|
| Any agent recommends "Roll Back" | **Roll Back** |
| Two or more agents recommend "Pause" | **Pause** |
| Otherwise | **Proceed** |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| LLM | Gemma 2B via Ollama |
| Data Processing | pandas |
| Web UI | Streamlit |
| HTTP Client | requests |
