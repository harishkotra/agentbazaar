from src.utils.ledger import Ledger

class EscrowAgent:
    def __init__(self):
        self.ledger = Ledger()

    def lock(self, contract_id: str, amount: float, task_id: str):
        self.ledger.lock_funds(contract_id, amount, task_id)
        return f"Funds ({amount}) locked for contract {contract_id}"

    def release(self, contract_id: str, worker_id: str):
        if self.ledger.release_funds(contract_id, worker_id):
            return f"Funds released to {worker_id}"
        return "Failed to release funds"

    def refund(self, contract_id: str):
        if self.ledger.refund_funds(contract_id):
            return "Funds refunded to Broker"
        return "Failed to refund"
