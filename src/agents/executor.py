from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import Contract, ExecutionResult

class ExecutorAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            description="You are a Task Executor. Your job is to actually do the work defined in the contract.",
            instructions=[
                "Read the contract deliverables carefully.",
                "Generate the required output (code, text, plan).",
                "Simulate the work execution.",
                "Return a summary of the work done."
            ]
        )

    def execute_task(self, contract: Contract) -> ExecutionResult:
        prompt = f"""
        Execute this contract:
        Deliverables: {contract.deliverables}
        
        Generate the actual content/code required.
        """
        response = self.agent.run(prompt)
        
        return ExecutionResult(
            task_id=contract.task_id,
            worker_id=contract.selected_worker,
            output=response.content,
            artifacts=["result.txt"]
        )
