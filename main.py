from app.network.peer_manager import PeerManager
import os
import uvicorn



from app import app, Config


node_id = int(os.environ["NODE_ID"])
init_peer = os.environ.get('INIT_PEER', '').strip()
config = Config.create_instance(node_id, init_peer)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=config.port, log_level='debug')



