import json
import os
from src.models.schemas import AgentStats

REP_FILE = "reputation_db.json"

class ReputationDB:
    def __init__(self):
        self._load()

    def _load(self):
        if os.path.exists(REP_FILE):
            with open(REP_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        with open(REP_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_stats(self, agent_id: str) -> AgentStats:
        data = self.data.get(agent_id, {})
        return AgentStats(**data) if data else AgentStats(agent_id=agent_id)

    def update_stats(self, agent_id: str, success: bool, score: float):
        stats = self.get_stats(agent_id)
        stats.tasks_completed += 1
        
        # Simple moving average update
        total_score = (stats.avg_score * (stats.tasks_completed - 1)) + score
        stats.avg_score = total_score / stats.tasks_completed
        
        if success:
            # Re-calculate success rate
            # Need to track total successes strictly? Let's just approximate for MVP or store basic counters
            # Let's fix the model to store success count to be accurate
            pass 
        
        # Heuristic update for success rate
        prev_successes = stats.success_rate * (stats.tasks_completed - 1)
        if success:
            prev_successes += 1
        stats.success_rate = prev_successes / stats.tasks_completed

        self.data[agent_id] = stats.model_dump()
        self._save()
