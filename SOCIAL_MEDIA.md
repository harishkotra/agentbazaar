# 🐦 Twitter Thread

1/8
I just built an autonomous AI Skills Marketplace running 100% locally on my Mac 🤯

Agents post jobs, bid for work, negotiate pay, sign contracts, and execute code—all without me touching the keyboard.

Built with @AgnoHQ and Ollama. Here’s how it works 🧵👇

2/8
The setup:
🤖 **Broker**: Turns my prompts into specs.
👷 **Workers**: 3 personas (Cheap, Premium, Balanced) competing for the gig.
🤝 **Negotiator**: actually HAGGLES with them to lower prices.
⚖️ **Judge**: Validates code before releasing escrow.

3/8
The Tech Stack:
- Python 🐍
- **Agno** (formerly Phidata) for the agent orchestration.
- **Ollama** running `llama3.2` for the brains.
- **Streamlit** for the dashboard.

No API keys. No cloud costs. Pure local agentic chaos.

4/8
Key Feature: **Strict Contracts** 📜
I used Agno’s `output_schema` with Pydantic models. The agents don't just chat; they trade structured JSON contracts with strict acceptance criteria.

If the output doesn't pass the tests, the simulated Escrow refunds the money!

5/8
The Negotiation Logic 🧠
The Negotiator agent uses a scoring formula:
`Score = (Price Weight) + (Reputation Weight) + (Confidence)`

It runs a multi-turn loop asking workers to drop prices by 10% until a deal is struck or patience runs out.

6/8
We tracked "Reputation" too. 
If a cheap agent wins but fails validation, their score tanks in the local DB. Next time, the Negotiator ignores them. 
Self-correcting markets in code.

7/8
The visualization:
Streamlit streams the events in real-time. You watch the "Thinking..." status, see the bids roll in, and watch the contract get signed live.

8/8
This architecture—Marketplaces of Agents—is where AI is heading.
Code is open source! run it yourself with `pip install agno` and `ollama run llama3.2`.

#AI #Agents #LocalLLM #Python #Agno

---

# 🔗 LinkedIn Post

**Subject: I built a fully autonomous AI Marketplace on my laptop. Here is what I learned.**

We often talk about "AI Agents," but usually we just mean a chatbot with tools. True agentic systems emerge when you have **conflict** and **cooperation**.

This weekend, I decided to simulate a gig economy where AI agents hire each other. I built **AgentBazaar** using the Agno Framework and Ollama.

**The Workflow:**
1.  **Broker Agent**: Takes a request ("Write a Python script...") and creates a technical spec.
2.  **Bidding War**: Multiple Worker Agents (with different personalities like "Fast & Cheap" vs "Premium") generating bids.
3.  **Negotiation**: A Negotiator agent that actively bargains to lower the price.
4.  **Escrow & Validation**: A Validator agent that specifically checks the work against the contract before releasing simulated funds.

**Why Agno?**
The challenge with complex agent/multi-agent systems is reliability. Agno’s ability to enforce `output_schema` using Pydantic models was a game changer. It meant my agents weren't just "chatting"—they were exchanging valid, executable JSON objects.

**The Result**
A self-contained economy running locally on `llama3.2`. Agents build reputation over time, bad actors get filtered out, and prices optimize themselves.

This is a prototype for how future software systems might self-assemble. Instead of monolithic code, imagine micro-services that negotiate their own APIs and SLAs dynamically.

All running locally, private, and fast.

#AI #MachineLearning #MultiAgentSystems #Agno #Ollama #Python #LLM
