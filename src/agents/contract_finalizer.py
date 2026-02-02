from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import TaskSpec, Bid, Contract
import uuid

class ContractFinalizerAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            description="Contract Finalizer",
            instructions=[
                "Draft a strict JSON contract.",
                "Include specific deliverables and penalty rules.",
                "Ensure payment matches the agreed bid.",
            ],
            output_schema=Contract,
        )

    def finalize_contract(self, task: TaskSpec, bid: Bid) -> Contract:
        prompt = f"""
        Task: {task.description}
        Agreed Bid: {bid.price} by {bid.agent_id}
        Timeline: {bid.timeline}
        
        Create a Contract object.
        contract_id should be unique.
        task_id: {task.task_id}
        selected_worker: {bid.agent_id}
        deliverables: Split the task description into 3-5 sub-deliverables.
        tests: Create 2-3 acceptance criteria tests.
        penalty_rules: Create 1-2 penalty rules for late delivery or failure.
        payment: {bid.price}
        status: "pending"
        """
        response = self.agent.run(prompt)
        contract = response.content
        if not contract.contract_id:
             contract.contract_id = str(uuid.uuid4())
        return contract
