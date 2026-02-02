from typing import List
from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import Bid, TaskSpec
import uuid

class WorkerAgent:
    def __init__(self, agent_id: str, persona: str, model_id="llama3.2:latest"):
        self.agent_id = agent_id
        self.persona = persona
        
        instructions = [
            f"You are a Worker Agent with the following persona: {persona}.",
            "Analyze the Task Specification provided.",
            "Decide if you want to bid on this task based on your persona.",
            "If you bid, create a realistic Bid object.",
            "Your price and timeline should reflect your persona (e.g., 'Fast/Cheap' is cheaper but maybe lower confidence).",
            "Return the result strictly as a Bid JSON object."
        ]

        self.agent = Agent(
            model=Ollama(id=model_id),
            description=f"Worker Agent {agent_id}",
            instructions=instructions,
            output_schema=Bid,
        )

    def generate_bid(self, task: TaskSpec) -> Bid:
        prompt = f"""
        Review this task:
        Description: {task.description}
        Budget: {task.budget}
        Deadline: {task.deadline}
        Criteria: {task.acceptance_criteria}

        Generate a bid for this task.
        Always ensure the agent_id in the Bid matches your ID: {self.agent_id}
        and task_id matches: {task.task_id}
        """
        response = self.agent.run(prompt)
        return response.content

def get_worker_team():
    return [
        WorkerAgent(agent_id="worker_fast_cheap", persona="Fast and Cheap. You prioritize speed and low cost. You might cut corners. You charge 50-70% of budget."),
        WorkerAgent(agent_id="worker_premium", persona="Premium and Thoroughbred. You are expensive and take your time, but produce high quality. You charge 90-110% of budget."),
        WorkerAgent(agent_id="worker_balanced", persona="Balanced and Reliable. You offer a fair price for good work. You charge 75-90% of budget.")
    ]
