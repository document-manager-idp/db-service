from app import create_app
import os
from init import setup_opensearch

setup_opensearch()

app = create_app()

HOSTNAME = os.environ.get('HOSTNAME', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5700'))

if __name__ == '__main__':
    app.run(host=HOSTNAME, port=PORT, debug=True)
