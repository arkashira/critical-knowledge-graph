# Runbook
A simple runbook management system.

## Features
* Add versions to a runbook
* Diff versions to see changes
* Search for steps in a runbook

## Usage
1. Create a new runbook: `runbook = Runbook("Test Runbook")`
2. Add a version to the runbook: `runbook.add_version(Version("2022-01-01 12:00:00", "John Doe", [Step("Step 1"), Step("Step 2")]))`
3. Diff two versions: `added_steps, removed_steps = runbook.diff_versions(version1, version2)`
4. Search for steps: `results = runbook.search("Step 1")`
