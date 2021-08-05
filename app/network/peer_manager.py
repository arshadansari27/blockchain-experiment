from typing import Dict, List, Tuple
import socket
import random


class PeerManager:
    def __init__(self, port):
        h_name = socket.gethostname()
        self.self_peer = socket.gethostbyname(h_name) + ":" + str(port)
        self.peers = []
        self.subscribed_to_peers = []
        self.connected_pairs = []

    def update_peers(self, peers):
        for peer in peers:
            if peer not in self.peers:
                self.peers.append(peer)

    def update_connection(self, connected_pairs: List[Tuple[str, str]]):
        for pair in connected_pairs:
            if pair in self.connected_pairs:
                continue
            self.connected_pairs.append(pair)
    
    def get_subcription_peers(self):
        subscribe_to = choose_peers_to_connect(
            self.self_peer, self.peers, self.connected_pairs
        )
        self.subscribed_to_peers = subscribe_to
        return subscribe_to


def choose_peers_to_connect(
    self_peer: str,
    peers: List[str],
    connected_pairs: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    candidate_connections = [u for u in connected_pairs]
    current_limit = 3
    counter = 0
    _peers = [u for u in peers if u != self_peer]
    while not is_good_connection(peers, candidate_connections):
        random.shuffle(_peers)
        candidate_peers = _peers[0:current_limit]
        candidate_connections = connected_pairs + [
            (self_peer, u) for u in candidate_peers
        ]
        counter += 1
        if counter % 3 == 0:
            current_limit += 1
    return [
        u[1] for u in candidate_connections
        if u[0] == self_peer
    ]


def is_good_connection(
    peers: List[str],
    connection_pairs: List[Tuple[str, str]]
):
    graph = {u: [] for u in peers}
    for (v1, v2) in connection_pairs:
        graph[v1].append(v2)
    if connected_components(graph) > 1:
        return False
    else:
        return True


def connected_components(graph: Dict[str, List[str]]) -> int:
    visited_vertexes = {k: False for k in graph}
    components = 0
    for v in graph:
        current_visited = sum(1 for v in visited_vertexes.values() if v)
        dfs_util(graph, v, visited_vertexes)
        updated_visited = sum(1 for v in visited_vertexes.values() if v)
        if updated_visited > current_visited:
            components += 1
    return components


def dfs_util(graph: Dict[str, List[str]], node: str, visited: Dict[str, bool]):
    if visited[node]:
        return
    visited[node] = True
    for connected_node in graph[node]:
        if visited[connected_node]:
            continue
        dfs_util(graph, connected_node, visited)
