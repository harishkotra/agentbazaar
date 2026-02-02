from agno.agent import Agent
from agno.models.ollama import Ollama
from src.models.schemas import TaskSpec
import uuid

class BrokerAgent:
    def __init__(self, model_id="llama3.2:latest"):
        self.agent = Agent(
            model=Ollama(id=model_id),
            description="You are a Task Broker. Your job is to analyze loose user requests and convert them into structured professional task specifications.",
            instructions=[
                "Analyze the user's request thoroughly.",
                "Extract or infer key details: description, budget, deadline, and acceptance criteria.",
                "If budget or deadline are not specified, estimate reasonable defaults based on complexity.",
                "Ensure acceptance criteria are objective and testable.",
                "Return the result strictly as a TaskSpec JSON object."
            ],
            output_schema=TaskSpec,
        )

    def create_task(self, user_request: str) -> TaskSpec:
        # We can perform additional logic here if needed, but for now direct delegation
        response = self.agent.run(f"Create a strict task specification for: {user_request}")
        # The Agno Agent with response_model returns a RunResponse, response.content is the model
        task = response.content
        if not task.task_id:
            task.task_id = str(uuid.uuid4())
        return task
