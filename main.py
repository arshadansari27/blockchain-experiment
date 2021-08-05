from app.network.peer_manager import PeerManager
import os
import uvicorn



from app import app, CONFIG

CONFIG.node_id = int(os.environ["NODE_ID"])
CONFIG.init_peer = os.environ.get('INIT_PEER', '').strip()
CONFIG.port = 5000 + CONFIG.node_id
CONFIG.peer_manager = PeerManager(CONFIG.port)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=CONFIG.port, log_level='debug')



