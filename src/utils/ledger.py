import json
import os
from typing import Dict

LEDGER_FILE = "escrow_ledger.json"

class Ledger:
    def __init__(self):
        self._load()

    def _load(self):
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"locked_funds": {}, "history": []}

    def _save(self):
        with open(LEDGER_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def lock_funds(self, contract_id: str, amount: float, task_id: str):
        self.data["locked_funds"][contract_id] = {
            "amount": amount,
            "task_id": task_id,
            "status": "LOCKED"
        }
        self._save()

    def release_funds(self, contract_id: str, recipient_id: str):
        if contract_id in self.data["locked_funds"]:
            entry = self.data["locked_funds"][contract_id]
            entry["status"] = "RELEASED"
            entry["recipient"] = recipient_id
            self.data["history"].append(entry)
            del self.data["locked_funds"][contract_id]
            self._save()
            return True
        return False

    def refund_funds(self, contract_id: str):
         if contract_id in self.data["locked_funds"]:
            entry = self.data["locked_funds"][contract_id]
            entry["status"] = "REFUNDED"
            self.data["history"].append(entry)
            del self.data["locked_funds"][contract_id]
            self._save()
            return True
         return False
