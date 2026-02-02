from typing import List, Optional
from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import Bid, TaskSpec, Contract
from src.agents.worker import WorkerAgent
from src.utils.reputation_db import ReputationDB

class NegotiatorAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            description="You are a shrewd Negotiator. Your goal is to get the best value for the Broker.",
            instructions=[
                "Compare the incoming bids against the TaskSpec.",
                "Identify the best candidate based on a balance of price, timeline, and confidence.",
                "You can ask for a lower price (e.g. 10% lower) or faster timeline.",
                "Be polite but firm."
            ]
        )
        self.rep_db = ReputationDB()

    def score_bid(self, bid: Bid, task_budget: float) -> float:
        """
        Score = (price_weight * normalized_price_inverse)
              + (reputation_weight * reputation)
              + (confidence_weight * confidence)
        """
        # Weights
        W_PRICE = 0.4
        W_REP = 0.3
        W_CONF = 0.3

        # Normalize Price (Lower is better)
        # If bid > budget, strict penalty? Or just relative?
        # Inverse: budget / bid. If bid is 50 and budget 100, score 2.0. If bid 200, score 0.5.
        price_score = task_budget / max(bid.price, 1.0)
        # Cap price score to avoid skewing
        price_score = min(price_score, 2.0) / 2.0 # Normalized to 0-1 approx

        # Reputation
        stats = self.rep_db.get_stats(bid.agent_id)
        rep_score = stats.avg_score / 100.0 if stats.tasks_completed > 0 else 0.5 # Default to 0.5

        # Confidence
        conf_score = bid.confidence

        final_score = (W_PRICE * price_score) + (W_REP * rep_score) + (W_CONF * conf_score)
        return final_score

    def negotiate(self, task: TaskSpec, bids: List[Bid], workers: List[WorkerAgent]) -> Bid:
        # 1. Score Bids
        scored_bids = []
        for b in bids:
            score = self.score_bid(b, task.budget)
            scored_bids.append((score, b))
        
        # Sort desc
        scored_bids.sort(key=lambda x: x[0], reverse=True)
        best_score, best_bid = scored_bids[0]
        
        # 2. Negotiate (Simple 1-round logic for demo purposes, but extensible)
        # If price is within budget, accept. Else, ask for reduction.
        if best_bid.price <= task.budget:
             return best_bid
        
        # Negotiation Loop (Max 3 rounds)
        current_bid = best_bid
        rounds = 0
        max_rounds = 3
        
        while current_bid.price > task.budget and rounds < max_rounds:
            rounds += 1
            # Ask for 10% reduction
            target_price = current_bid.price * 0.90
            
            # Simulate Worker Response (simplified)
            # In a real agent system, we'd call worker.revise_bid(msg)
            # Here: if target > 70% of original ask, they accept.
            
            # We assume the best_bid.price is their "ask".
            # For the demo, let's say they agree to meet halfway to budget if it's reasonable.
            
            new_price = max(target_price, task.budget) # Don't go below budget if not needed
            current_bid.price = new_price
            current_bid.plan += f" [Negotiated: Dropped price to {new_price}]"

        return current_bid
