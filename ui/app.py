import streamlit as st
import sys
import os
import json
import time
import asyncio
import importlib

# --- FORCE RELOAD MODULES ---
# This ensures that when we update agent logic, the UI picks it up immediately
# without needing a full server restart.
def reload_modules():
    modules = [
        "src.orchestration",
        "src.agents.negotiator", 
        "src.agents.worker",
        "src.agents.broker",
        "src.agents.contract_finalizer",
        "src.agents.executor",
        "src.agents.validator",
        "src.agents.escrow",
        "src.agents.reputation"
    ]
    for m in modules:
        if m in sys.modules:
            importlib.reload(sys.modules[m])

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Reload logic to ensure 'score_bid' and others are available
reload_modules()

from src.orchestration import MarketSimulation
from src.utils.ledger import Ledger
from src.utils.reputation_db import ReputationDB
from src.agents.worker import get_worker_team

st.set_page_config(page_title="AgentBazaar", layout="wide", page_icon="🤖")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #4FACFE; }
    .sub-title { font-size: 1.5rem; color: #ddd; margin-bottom: 20px; }
    .agent-card { 
        padding: 10px; 
        border-radius: 8px; 
        background-color: #1E1E1E; 
        margin-bottom: 10px; 
        border-left: 4px solid #4FACFE;
    }
    .agent-name { font-weight: bold; font-size: 1.1em; color: #FFF; }
    .agent-persona { font-size: 0.9em; color: #AAA; font-style: italic; }
    .step-log { font-family: 'Courier New', monospace; font-size: 0.9rem; color: #00FF00; }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<div class="main-title">🤖 AgentBazaar</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Autonomous Agent Marketplace Simulation</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 📊 Live Market Stats")
trigger_refresh = st.sidebar.button("🔄 Refresh Data")

ledger = Ledger()
rep_db = ReputationDB()

with st.sidebar.expander("🏆 Reputation Leaderboard", expanded=True):
    if rep_db.data:
        sorted_reps = sorted(rep_db.data.items(), key=lambda x: x[1]['avg_score'], reverse=True)
        for agent_id, data in sorted_reps:
            st.markdown(f"**{agent_id}**")
            cols = st.columns([3, 1])
            cols[0].progress(int(data['avg_score']))
            cols[1].caption(f"{data['avg_score']:.0f}%")
    else:
        st.info("No reputation data yet.")

with st.sidebar.expander("💰 Escrow Ledger", expanded=True):
    if ledger.data["locked_funds"]:
        for cid, data in ledger.data["locked_funds"].items():
            st.code(f"Contract: {cid[:6]}...\nAmount: ${data['amount']}\nStatus: {data['status']}")
    else:
        st.caption("No funds currently locked.")

# --- Active Agents Roster ---
st.markdown("### 👥 Active Agents Marketplace")
workers = get_worker_team()
cols = st.columns(len(workers))
for idx, worker in enumerate(workers):
    with cols[idx]:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-name">{worker.agent_id}</div>
            <div class="agent-persona">{worker.persona}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📝 New Request")
    default_prompt = "Create a python function to check if a number is prime and write a unit test for it."
    user_request = st.text_area("Describe the task", value=default_prompt, height=150)
    
    start_btn = st.button("🚀 Launch Agents", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📡 Live Simulation Feed")
    feed_placeholder = st.empty()

if start_btn and user_request:
    sim = MarketSimulation()
    
    with feed_placeholder.container():
        # Use st.status for the main container to show active "Loading..." state
        with st.status("Agents are working...", expanded=True) as status:
            
            # Container for scrollable logs or cards
            history_container = st.container()
            
            for event in sim.run_stream(user_request):
                step = event.get("step")
                msg = event.get("message")
                
                # Update status label to show what is happening currently
                status.update(label=f"**{step}**: {msg}")
                
                # Icon mapping
                icon = "🔹"
                if step == "WORKERS": icon = "👷"
                elif step == "NEGOTIATOR": icon = "🤝"
                elif step == "CONTRACT": icon = "📜"
                elif step == "EXECUTOR": icon = "⚙️"
                elif step == "VALIDATOR": icon = "✅"
                elif step == "ESCROW": icon = "💰"
                elif step == "FINAL": icon = "🏁"
                
                # Write to history with formatted markdown
                # st.write or st.markdown appends to the bottom, acting like scrolling log
                history_container.markdown(f"### {icon} {step}")
                history_container.info(msg)
                
                # Render Data if available
                if "data" in event:
                    history_container.markdown("**📦 Data Payload**")
                    history_container.json(event["data"])

                # UX Pause
                time.sleep(0.8) 
                
                if step == "FINAL":
                    if event["status"] == "success":
                        status.update(label="✅ Transaction Complete!", state="complete", expanded=True)
                        st.balloons()
                    else:
                        status.update(label="❌ Transaction Failed", state="error", expanded=True)
