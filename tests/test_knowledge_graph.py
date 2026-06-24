import pytest
from knowledge_graph import KnowledgeGraph, Runbook

def test_search():
    graph = KnowledgeGraph()
    graph.add_runbook(Runbook('Runbook 1', 1, ['Step 1', 'Step 2']))
    graph.add_runbook(Runbook('Runbook 2', 2, ['Step 3', 'Step 4']))
    results = graph.search('Step')
    assert len(results) == 4
    assert results[0]['title'] == 'Runbook 2'
    assert results[0]['version'] == 2
    assert results[0]['step'] == 'Step 3'
    assert results[0]['matching_steps'] == ['Step 3', 'Step 4']

def test_search_empty():
    graph = KnowledgeGraph()
    results = graph.search('Step')
    assert len(results) == 0

def test_search_performance():
    graph = KnowledgeGraph()
    for i in range(1000):
        graph.add_runbook(Runbook(f'Runbook {i}', i, [f'Step {i}']))
    import time
    start_time = time.time()
    results = graph.search('Step')
    end_time = time.time()
    assert end_time - start_time < 0.5
