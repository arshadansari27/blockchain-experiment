import asyncio
from datetime import datetime
from aiohttp import request
from aiohttp.client import ClientSession
from typing import List
from .peer_manager import PeerManager


async def load_peers(init_peer: str, peer_manager: PeerManager) -> List[str]:
    connections = []
    async with ClientSession(trust_env=True) as session:
        async with session.post(
            f"http://{init_peer}/admin/register/{peer_manager.self_peer}"
        ) as response:
            result = await response.json()
            peer_manager.update_peers(result["peers"])
            for peer in result["peers"]:
                if peer == peer_manager.self_peer:
                    print("Skipping self:", peer)
                    continue
                async with session.get(
                    f"http://{peer}/admin/connections"
                ) as response:
                    result = await response.json()
                    for connected_peer in result["connections"]:
                        connections.append(tuple([peer, connected_peer]))
        if connections:
            peer_manager.update_connection(connections)
    peer_manager.set_subcription_peers()
