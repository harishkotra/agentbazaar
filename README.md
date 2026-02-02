# 🤖 AgentBazaar: Emergent Skill Marketplace

![AgentBazaar Banner](https://img.shields.io/badge/Status-Active-success) ![Stack](https://img.shields.io/badge/Stack-Agno%20%7C%20Ollama%20%7C%20Streamlit-blue)

**AgentBazaar** is a local multi-agent simulation where AI agents autonomously trade skills. It simulates a gig economy where agents post tasks, bid for work, negotiate contracts, execute deliverables, and validate results—all without human intervention.

Built using the **Agno Framework** (formerly Phidata) for orchestration and **Ollama** for local LLM inference.

## 🏗 Architecture

The system follows a strict linear orchestration flow designed to mimic high-stakes contracting environments:

```mermaid
graph TD
    User((User)) -->|Prompt| Broker[Broker Agent]
    Broker -->|TaskSpec| Workers[Worker Market]
    subgraph Market Logic
        Workers -->|Bids| Negotiator[Negotiator Agent]
        Negotiator -->|Winning Bid| Contract[Contract Agent]
    end
    subgraph Execution
        Contract -->|Contract JSON| Escrow[Escrow Agent]
        Escrow -->|Lock Funds| Executor[Executor Agent]
        Executor -->|Result| Validator[Validator Agent]
    end
    Validator -->|Pass/Fail| Escrow
    Escrow -->|Release/Refund| User
    Validator -->|Score| Reputation[Reputation DB]
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Broker fill:#fff,stroke:#333
    style Workers fill:#ccf,stroke:#333
    style Escrow fill:#dfd,stroke:#333
```

## 🧠 Components & Tech Matrix

### 1. Agents (Agno Framework)
We utilize Agno's `Agent` class to define specialized personas.
*   **Broker**: Structurers messy user prompts into strict JSON `TaskSpec`.
*   **Workers**: 3 distinct personas (Fast/Cheap, Premium, Balanced) that generate competitive bids.
*   **Negotiator**: Implements a scoring algorithm (`price` vs `reputation` vs `confidence`) and runs a multi-turn negotiation loop to drive down prices.
*   **Validator**: Acts as a strict QA, checking output against contract acceptance criteria.

### 2. LLM Engine (Ollama)
The system is built to run 100% locally.
*   **Model**: `llama3.2:latest` (Swappable in `src/agents/*.py`)
*   **Inference**: Zero-latency local calls via standard Ollama API.

### 3. State & Persistence
*   **Escrow Ledger**: Simulated financial locking mechanism (`json` based).
*   **Reputation DB**: Tracks long-term agent performance (Success Rate, Avg Score).

## 🚀 Getting Started

### Prerequisites
*   Python 3.9+
*   [Ollama](https://ollama.ai) installed and running.

### Installation

1.  **Clone the repository**
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Pull the Model**
    ```bash
    ollama pull llama3.2:latest
    ```

### Running the Simulation
Launch the visual dashboard:
```bash
streamlit run ui/app.py
```

## 💡 How It Works

1.  **Task Ingestion**: You post "Write a clear Python function for finding primes".
2.  **Bidding War**:
    *   *Worker A (Cheap)* bids $40, Low Confidence.
    *   *Worker B (Premium)* bids $120, High Confidence.
3.  **Negotiation**: The Negotiator scores bids. It might challenge Worker B to lower their price to $100.
4.  **Contracting**: A formal JSON contract is generated with "Acceptance Tests" derived from your prompt.
5.  **Execution**: The winning agent writes the code.
6.  **Validation**: The Validator runs a rubric check. If it passes, Escrow releases funds and Reputation increases.

## 🛠 Building with Agno

This project demonstrates key Agno patterns:

*   **Structured Outputs**: Using `output_schema` to force LLMs to reply in valid Pydantic models (crucial for system reliability).
*   **Role Playing**: Assigning distinct `instructions` to agents to create "Personas" that behave differently.
*   **Orchestration**: Managing state hand-offs between multiple agents in a Pythonic workflow.

## 🔮 Future Use Cases
*   **Automated DevOps**: Agents bidding on ticket resolution.
*   **Content Factories**: SEO agents, Writers, and Editors negotiating details.
*   **Resource Allocation**: Autonomous trading bots negotiating API usage.

### Output Screenshots

<img width="2432" height="1958" alt="screencapture-localhost-8501-2026-02-02-18_03_44" src="https://github.com/user-attachments/assets/e4f8cfca-eef3-4929-8af1-2fa2eb16ec38" />
<img width="2432" height="1958" alt="screencapture-localhost-8501-2026-02-02-18_03_50" src="https://github.com/user-attachments/assets/ab5d3ac0-f382-4e8b-a184-0a538417f896" />
<img width="2432" height="3266" alt="screencapture-localhost-8501-2026-02-02-18_03_58" src="https://github.com/user-attachments/assets/97f79633-d1c1-4d59-9f34-ef6010fbbc7f" />
<img width="2432" height="4786" alt="screencapture-localhost-8501-2026-02-02-18_04_07" src="https://github.com/user-attachments/assets/adfb2847-c00f-4801-a9bc-6a696c238437" />
<img width="2432" height="9700" alt="screencapture-localhost-8501-2026-02-02-18_04_22" src="https://github.com/user-attachments/assets/097e0f82-b01a-400d-bd35-d99dfce20699" />
<img width="2432" height="16498" alt="screencapture-localhost-8501-2026-02-02-18_04_50" src="https://github.com/user-attachments/assets/e9a3c23e-28c4-4be1-9748-e0e650145556" />
<img width="2432" height="9094" alt="screencapture-localhost-8501-2026-02-02-18_05_22" src="https://github.com/user-attachments/assets/6481f7a0-349d-4586-bf42-ba4e3350fc70" />
<img width="2432" height="1958" alt="screencapture-localhost-8501-2026-02-02-18_06_02" src="https://github.com/user-attachments/assets/a7952b64-c4f2-40f7-af96-b5b103e4900a" />


