import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class AuditTrailEntry:
    user: str
    action: str
    timestamp: str
    metadata: dict

class AuditTrail:
    def __init__(self):
        self.entries = []

    def add_entry(self, user: str, action: str, metadata: dict):
        entry = AuditTrailEntry(
            user=user,
            action=action,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metadata=metadata,
        )
        self.entries.append(entry)

    def export_to_pdf(self):
        # Simulate PDF generation for demonstration purposes
        pdf_content = "Audit Trail:\n"
        for entry in self.entries:
            pdf_content += f"{entry.user} - {entry.action} - {entry.timestamp}\n"
            pdf_content += json.dumps(entry.metadata, indent=4) + "\n\n"
        return pdf_content

    def digitally_sign(self, pdf_content: str):
        # Simulate digital signing for demonstration purposes
        return f"Digitally signed: {pdf_content}"

def generate_audit_trail(entries: List[dict]):
    audit_trail = AuditTrail()
    for entry in entries:
        audit_trail.add_entry(
            user=entry["user"],
            action=entry["action"],
            metadata=entry["metadata"],
        )
    pdf_content = audit_trail.export_to_pdf()
    signed_pdf_content = audit_trail.digitally_sign(pdf_content)
    return signed_pdf_content
