import pytest
from audit_trail import generate_audit_trail

def test_generate_audit_trail():
    entries = [
        {"user": "John Doe", "action": "Created", "metadata": {"runbook_id": 1}},
        {"user": "Jane Doe", "action": "Updated", "metadata": {"runbook_id": 2}},
    ]
    pdf_content = generate_audit_trail(entries)
    assert "John Doe - Created" in pdf_content
    assert "Jane Doe - Updated" in pdf_content
    assert "Digitally signed" in pdf_content

def test_generate_audit_trail_empty():
    entries = []
    pdf_content = generate_audit_trail(entries)
    assert pdf_content == "Digitally signed: Audit Trail:\n"

def test_generate_audit_trail_invalid_input():
    entries = None
    with pytest.raises(TypeError):
        generate_audit_trail(entries)
