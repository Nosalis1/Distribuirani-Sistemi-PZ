from flask import Flask

from .config import Config
from .model import *
from .view import view_bp, api_bp

import requests

distributed_files = {}
CONFIGURATION = Config(5000, 'shared')


def update():
    global distributed_files
    distributed_files = load_shared_directory(CONFIGURATION.SHARED_DIR)
    print("Updating peer")

    files = []
    for file in distributed_files:
        files.append(file.json())

    data = {'peer': CONFIGURATION.PORT, 'files': files}
    response = requests.post(f'{CONFIGURATION.SERVER_ADDRESS}/update', json=data)
    if response.status_code == 200:
        print("Successfully updated peer")
    else:
        print("Failed to update peer")
    pass


def register_peer():
    print("Registering peer")

    files = []
    for file in distributed_files:
        files.append(file.json())

    data = {'peer': CONFIGURATION.PORT, 'files': files}
    response = requests.post(f'{CONFIGURATION.SERVER_ADDRESS}/register', json=data)
    if response.status_code == 200:
        print("Successfully registered peer")
    else:
        print("Failed to register peer")
    pass


def create_app(port, shared):
    global CONFIGURATION, distributed_files
    CONFIGURATION.PORT = port
    CONFIGURATION.SHARED_DIR = shared

    distributed_files = load_shared_directory(CONFIGURATION.SHARED_DIR)
    print(distributed_files)

    app = Flask(__name__)
    app.config.from_object(CONFIGURATION)

    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    register_peer()
    return app
