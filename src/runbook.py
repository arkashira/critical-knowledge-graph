import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Step:
    description: str

@dataclass
class Version:
    timestamp: str
    author: str
    steps: List[Step]

class Runbook:
    def __init__(self, name: str):
        self.name = name
        self.versions = []

    def add_version(self, version: Version):
        self.versions.append(version)

    def get_versions(self):
        return self.versions

    def diff_versions(self, version1: Version, version2: Version):
        added_steps = [step for step in version2.steps if step not in version1.steps]
        removed_steps = [step for step in version1.steps if step not in version2.steps]
        return added_steps, removed_steps

    def search(self, query: str):
        results = []
        for version in self.versions:
            for step in version.steps:
                if query in step.description:
                    results.append((version, step))
        return results
