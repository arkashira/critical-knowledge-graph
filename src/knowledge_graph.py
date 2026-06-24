import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Runbook:
    title: str
    version: int
    steps: List[str]

class KnowledgeGraph:
    def __init__(self):
        self.runbooks = []

    def add_runbook(self, runbook: Runbook):
        self.runbooks.append(runbook)

    def search(self, query: str) -> List[dict]:
        results = []
        for runbook in self.runbooks:
            for step in runbook.steps:
                if query.lower() in step.lower():
                    results.append({
                        'title': runbook.title,
                        'version': runbook.version,
                        'step': step,
                        'matching_steps': [step for step in runbook.steps if query.lower() in step.lower()]
                    })
        results.sort(key=lambda x: (x['version'], len(x['matching_steps'])), reverse=True)
        return results
