from app.network.peer_manager import (
    PeerManager,
    choose_peers_to_connect,
    connected_components,
    dfs_util,
    is_good_connection,
)


def test_dfs_util():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": ["C", "B"],
    }
    visited = {"A": False, "B": False, "C": False, "D": False}
    dfs_util(graph, "A", visited)

    assert all(u for u in visited.values())

    graph = {
        "A": ["B"],
        "B": [],
        "C": ["D"],
        "D": ["C"],
    }
    visited = {"A": False, "B": False, "C": False, "D": False}
    dfs_util(graph, "A", visited)
    assert visited == {"A": True, "B": True, "C": False, "D": False}


def test_connected_components():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["A"],
        "D": [],
    }
    assert connected_components(graph) == 1
    graph = {
        "A": ["B"],
        "B": [],
        "C": ["D"],
        "D": [],
    }
    assert connected_components(graph) == 2


def test_is_good_connection():
    assert not is_good_connection(
        ["A", "B", "C", "D", "E", "F"], [("B", "A"), ("D", "E"), ("B", "C")]
    )
    assert not is_good_connection(
        ["A", "B", "C", "D", "E", "F"],
        [("B", "A"), ("D", "E"), ("B", "C"), ("C", "F"), ("F", "E")],
    )
    assert not is_good_connection(
        ["A", "B", "C", "D", "E", "F"],
        [("A", "B"), ("D", "E"), ("B", "C"), ("C", "F"), ("F", "E")],
    )


def test_choose_peers_to_connect():
    self_peer = "A"
    peers = ["A", "B", "C", "D", "E", "F"]

    def check_for_goodness(_chosen, _connected_pairs):
        tuples = [(self_peer, u) for u in _chosen]
        return is_good_connection(peers, _connected_pairs + tuples)

    c1 = [("B", "A"), ("D", "E"), ("B", "C"), ("C", "F"), ("F", "E")]
    chosen1 = choose_peers_to_connect(self_peer, peers, c1)
    assert check_for_goodness(chosen1, c1) == True


def test_peers_selection_1():
    manager = PeerManager("A", ["B", "C", "D", "E", "F"])
    c1 = [("B", "A"), ("D", "E"), ("B", "C")]
    result = manager.choose_peers_to_connect()
    assert manager.is_good_connection(result + c1) == True


def test_peers_selection_2():
    manager = PeerManager("A", ["B", "C", "D", "E", "F"])
    connections = [("B", "F"), ("D", "E"), ("B", "C")]
    result = manager.choose_peers_to_connect()
    assert manager.is_good_connection(result + connections) == True
