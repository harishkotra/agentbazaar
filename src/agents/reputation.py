from src.utils.reputation_db import ReputationDB

class ReputationAgent:
    def __init__(self):
        self.db = ReputationDB()

    def update(self, agent_id: str, success: bool, score: float):
        self.db.update_stats(agent_id, success, score)
        return f"Reputation updated for {agent_id}"

    def get_reputation(self, agent_id: str):
        return self.db.get_stats(agent_id)
