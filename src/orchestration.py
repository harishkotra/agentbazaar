from typing import Dict, Any, Generator
from src.agents.broker import BrokerAgent
from src.agents.worker import get_worker_team
from src.agents.negotiator import NegotiatorAgent
from src.agents.contract_finalizer import ContractFinalizerAgent
from src.agents.executor import ExecutorAgent
from src.agents.validator import ValidatorAgent
from src.agents.escrow import EscrowAgent
from src.agents.reputation import ReputationAgent
from src.models.schemas import TaskSpec, Bid, Contract, ExecutionResult, ValidationResult

class MarketSimulation:
    def __init__(self):
        self.broker = BrokerAgent()
        self.workers = get_worker_team()
        self.negotiator = NegotiatorAgent()
        self.contractor = ContractFinalizerAgent()
        self.executor = ExecutorAgent()
        self.validator = ValidatorAgent()
        self.escrow = EscrowAgent()
        self.reputation = ReputationAgent()

    def run_stream(self, user_request: str) -> Generator[Dict[str, Any], None, None]:
        log = []
        
        # 1. Broker
        yield {"step": "BROKER", "status": "active", "message": f"Broker analyzing request: {user_request}"}
        task = self.broker.create_task(user_request)
        yield {"step": "BROKER", "status": "done", "message": f"Task Created: {task.task_id}", "data": task.model_dump()}
        
        # 2. Bidding
        yield {"step": "WORKERS", "status": "active", "message": "Agents are evaluating the task..."}
        bids = []
        for worker in self.workers:
            yield {"step": "WORKERS", "status": "thinking", "message": f"{worker.agent_id} ({worker.persona}) is formulating a bid..."}
            bid = worker.generate_bid(task)
            bids.append(bid)
            yield {"step": "WORKERS", "status": "bid", "message": f"Bid from {worker.agent_id}: ${bid.price}", "data": bid.model_dump()}

        if not bids:
            yield {"step": "ERROR", "message": "No bids received."}
            return

        # 3. Negotiation
        yield {"step": "NEGOTIATOR", "status": "active", "message": "Negotiator scoring bids..."}
        
        # Calculate scores for display
        scored_bids_data = []
        for b in bids:
            score = self.negotiator.score_bid(b, task.budget)
            scored_bids_data.append({"agent": b.agent_id, "score": f"{score:.2f}", "price": b.price})
        yield {"step": "NEGOTIATOR", "status": "scoring", "message": "Bid Scores Calculated", "data": scored_bids_data}
        
        winning_bid = self.negotiator.negotiate(task, bids, self.workers)
        
        if winning_bid.price > task.budget:
             yield {"step": "NEGOTIATOR", "status": "warning", "message": f"Negotiation finalized but over budget: {winning_bid.price} > {task.budget}"}
        
        yield {"step": "NEGOTIATOR", "status": "done", "message": f"Winner selected: {winning_bid.agent_id} at ${winning_bid.price}", "data": winning_bid.model_dump()}

        # 4. Contract
        yield {"step": "CONTRACT", "status": "active", "message": "Drafting contract..."}
        contract = self.contractor.finalize_contract(task, winning_bid)
        yield {"step": "CONTRACT", "status": "done", "message": f"Contract {contract.contract_id} signed.", "data": contract.model_dump()}

        # 5. Escrow Lock
        yield {"step": "ESCROW", "status": "active", "message": "Locking funds..."}
        lock_msg = self.escrow.lock(contract.contract_id, contract.payment, task.task_id)
        yield {"step": "ESCROW", "status": "done", "message": lock_msg}

        # 6. Execution
        yield {"step": "EXECUTOR", "status": "active", "message": f"Worker {contract.selected_worker} executing task..."}
        result = self.executor.execute_task(contract)
        yield {"step": "EXECUTOR", "status": "done", "message": "Work complete.", "data": result.model_dump()}

        # 7. Validation
        yield {"step": "VALIDATOR", "status": "active", "message": "Validating output..."}
        validation = self.validator.validate_work(contract, result)
        yield {"step": "VALIDATOR", "status": "done", "message": f"Validation Score: {validation.score}", "data": validation.model_dump()}

        # 8. Settlement
        if validation.passed:
            release_msg = self.escrow.release(contract.contract_id, contract.selected_worker)
            yield {"step": "ESCROW", "status": "release", "message": release_msg}
            
            self.reputation.update(contract.selected_worker, True, validation.score)
            yield {"step": "REPUTATION", "status": "update", "message": "Reputation increased."}
            
            yield {"step": "FINAL", "status": "success", "message": "Transaction Successfully Closed."}
        else:
            refund_msg = self.escrow.refund(contract.contract_id)
            yield {"step": "ESCROW", "status": "refund", "message": refund_msg}
            
            self.reputation.update(contract.selected_worker, False, validation.score)
            yield {"step": "REPUTATION", "status": "update", "message": "Reputation penalized."}
            
            yield {"step": "FINAL", "status": "failed", "message": "Transaction Failed."}
