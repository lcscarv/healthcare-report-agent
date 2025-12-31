from langgraph.graph import END
from app.agents.report_workflow import should_continue


class MockState:
    def __init__(self, is_valid: bool, iteration_count: int):
        self.is_valid = is_valid
        self.iteration_count = iteration_count


def create_mock_graph():
    class MockGraph:
        def __init__(self):
            self.edges = []

        def add_edge(self, from_node, to_node):
            self.edges.append((from_node, to_node))

    mock_graph = MockGraph()

    return mock_graph


def test_should_continue_true():
    state = MockState(is_valid=True, iteration_count=1)
    result = should_continue(state)
    mock_graph = create_mock_graph()
    mock_graph.add_edge("audit_summary_node", result)
    assert result == END


def test_should_continue_max_iteration():
    state = MockState(is_valid=False, iteration_count=3)
    result = should_continue(state)
    mock_graph = create_mock_graph()
    mock_graph.add_edge("audit_summary_node", result)
    assert result == END


def test_should_continue_false():
    state = MockState(is_valid=False, iteration_count=1)
    result = should_continue(state)
    mock_graph = create_mock_graph()
    mock_graph.add_edge("audit_summary_node", result)
    assert result == "summarizer_node"
