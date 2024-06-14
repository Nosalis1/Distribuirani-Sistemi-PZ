from flask import Blueprint, render_template, send_from_directory
from .utils import read_file
from .replicator import replicator
import requests

view_bp = Blueprint("view_bp", __name__)


@view_bp.route("/")
def home():
    from . import distributed_files
    return render_template('index.html', data=distributed_files)


@view_bp.route("/<file_name>")
def home_file(file_name):
    from . import CONFIGURATION, distributed_files
    return render_template('index.html', data=distributed_files,
                           file=read_file(f'{CONFIGURATION.SHARED_DIR}/{file_name}'))


@view_bp.route('/search/<file_name>', methods=['GET'])
def search(file_name):
    from . import CONFIGURATION, update

    response = requests.get(f'{CONFIGURATION.SERVER_ADDRESS}/search', params={'filename': file_name})
    if response.status_code == 200:
        peers = response.json().get('peers', [])

        if not peers or len(peers) == 0:
            return {'message': 'File not found'}, 404

        response = requests.get(f'http://127.0.0.1:{peers[0]}/download/{file_name}')
        if response.status_code == 200:
            with open(f'./{CONFIGURATION.SHARED_DIR}/{file_name}', 'wb') as f:
                f.write(response.content)

            update()
        else:
            print('Failed to download file')
            return {'message': 'Failed to download file'}, 500
    else:
        print('Failed to search file')
        return {'message': 'Failed to search file'}, 500
    return {'message': 'Success'}, 200


api_bp = Blueprint("api_bp", __name__)


@api_bp.route('/download/<file_name>', methods=['GET'])
@replicator
def download_file(file_name):
    from . import CONFIGURATION
    return send_from_directory(f'../{CONFIGURATION.SHARED_DIR}', file_name, as_attachment=True)


@api_bp.route('/replicate/<peer>/<file_name>', methods=['POST'])
def replicate(peer, file_name):
    from . import CONFIGURATION, update
    response = requests.get(f'http://127.0.0.1:{peer}/download/{file_name}')
    if response.status_code == 200:
        with open(f'./{CONFIGURATION.SHARED_DIR}/{file_name}', 'wb') as f:
            f.write(response.content)
        update()
    else:
        print('Failed to download file')
