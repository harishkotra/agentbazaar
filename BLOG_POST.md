# Building an Autonomous AI Agent Marketplace with Agno & Ollama

Imagine a marketplace where you post a job, and AI agents not only do the work but also **compete** for it, **negotiate** their pay, and **sign contracts**—all securely on your local machine.

In this post, I’ll break down how I built **AgentBazaar**, a multi-agent simulation using the **Agno Framework** (formerly Phidata) and **Ollama**.

## The Concept: An Economy of Agents
Most agent demos show a single chain: *Plan -> Execute*. I wanted to model **social dynamics**. What happens when agents have conflicting goals?
*   **Broker**: Wants high quality.
*   **Worker**: Wants high pay.
*   **Negotiator**: Wants to optimize value.

To simulate this, we needed a robust orchestration layer. Enter Agno.

## The Stack
*   **Agno**: For defining agents, memory, and structured outputs.
*   **Ollama (`llama3.2`)**: For local, free inference.
*   **Streamlit**: For visualizing the chaos in real-time.

## Key Technical Implementation

### 1. Structured Is Better Than Clever
One of the biggest pain points in agentic AI is output reliability. Agno solves this elegantly with `output_schema`.

Instead of hoping the LLM returns JSON, we enforce it via Pydantic models. Here is our **Broker Agent**:

```python
class BrokerAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            instructions=[
                "Analyze user requests.",
                "Extract description, budget, and acceptance criteria.",
                "Return valid JSON."
            ],
            output_schema=TaskSpec, # <--- The Magic
        )
```

By defining `TaskSpec` as a Pydantic model by passing it to `output_schema`, Agno handles the prompt engineering required to get perfect JSON back.

### 2. Multi-turn Negotiation Loop
We implemented a loop where the Negotiator agent doesn't just pick the cheapest option; it actively haggles.

```python
# Simplified Logic
while current_bid.price > task.budget and rounds < 3:
    target_price = current_bid.price * 0.90 # Ask for 10% off
    # ... logic to see if Worker accepts ...
    current_bid.price = new_price 
```
This adds a layer of realism often missing in static chains.

### 3. The Validator / Escrow Pattern
Trust is key. We didn't want the Worker to just say "I'm done." We added a **Validator Agent** that acts as an impartial judge.

The **Escrow Agent** holds the "funds" (simulated in a JSON ledger) and only releases them if the Validator returns `passed=True`.

```python
def validate_work(self, contract, result):
    # LLM compares Result vs Contract Criteria
    response = self.agent.run(f"verify {result} against {contract.tests}")
    return response.content # Returns ValidationResult JSON
```

## Visualizing the "Mind" of the Market
We used **Streamlit** with `streamlit.status` to create a streaming feed. Since agent actions take time (even locally), showing the "thinking" process is crucial for UX.

We utilized Python generators (`yield`) in our orchestration layer so the UI updates instantly after every step, rather than waiting for the whole flow to finish.

```python
# Orchestration yielding events
yield {"step": "NEGOTIATOR", "message": "Scoring bids..."}
winning_bid = self.negotiator.negotiate(...)
yield {"step": "NEGOTIATOR", "message": "Winner found!", "data": winning_bid}
```

## Why This Matters
This isn't just a toy. This architecture—**negotiation, contracting, validation**—is the blueprint for future autonomous organizations. 

Whether it's software services micro-bidding on API calls or content agents negotiating editorial standards, the future is multi-agent. And with tools like Agno and Ollama, you can build it on your laptop today.

---
*Check out the code on GitHub to run your own local marketplace.*
