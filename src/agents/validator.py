from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import Contract, ExecutionResult, ValidationResult

class ValidatorAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            description="You are a QA Validator. You strictly check if the deliverables match the contract.",
            instructions=[
                "Compare the Execution Result against the Contract Deliverables and Tests.",
                "Be critical.",
                "Assign a score from 0-100.",
                "If criteria are met, passed=True, else False.",
                "Return a ValidationResult JSON."
            ],
            output_schema=ValidationResult,
        )

    def validate_work(self, contract: Contract, result: ExecutionResult) -> ValidationResult:
        prompt = f"""
        Contract Tests: {contract.tests}
        Deliverables: {contract.deliverables}
        
        Work Output:
        {result.output}
        
        Did the worker satisfy the requirements?
        """
        response = self.agent.run(prompt)
        return response.content
