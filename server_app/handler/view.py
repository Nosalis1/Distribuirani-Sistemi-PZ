from flask import Blueprint, request, jsonify
import requests
from multiprocessing import Pool, cpu_count

services = Blueprint('services', __name__)

file_index = {}


@services.route('/register', methods=['POST'])
def register():
    peer = request.json['peer']
    files = request.json['files']

    if not peer or not files:
        return jsonify({'status': 'error', 'message': 'Empty request'}), 501

    file_index[peer] = files

    print(f'Registered peer {peer} with files {files}')

    return jsonify({'status': 'registered'}), 200


@services.route('/update', methods=['POST'])
def update():
    peer = request.json['peer']
    files = request.json['files']

    if not peer or not files:
        return jsonify({'status': 'error', 'message': 'Empty request'}), 501

    file_index[peer] = files

    print(f'Updated peer {peer} with files {files}')

    return jsonify({'status': 'updated'}), 200


def do_replication(peers_with_file, owner, filename):
    for peer in peers_with_file:
        if peer != owner:
            requests.post(f'http://127.0.0.1:{peer}/replicate/{owner}/{filename}')
    pass


@services.route('/replicate', methods=['POST'])
def replicate():
    owner = request.json['owner']
    filename = request.json['filename']

    if not owner or not filename:
        return jsonify({'status': 'error', 'message': 'Empty request'}), 501

    do_replication(file_index.keys(), owner, filename)

    print(f'Replicated from peer {owner}')

    return jsonify({'status': 'replicated'}), 200


def search_files(args):
    peer, files, filename = args
    for f in files:
        if f['file_name'] == filename:
            return peer
    return None


@services.route('/search', methods=['GET'])
def search():
    filename = request.args.get('filename')

    if not filename:
        return jsonify({'status': 'error', 'message': 'Empty request'}), 501

    pool = Pool(cpu_count())  # pool of workers
    peers_with_file = pool.map(search_files, [(peer, files, filename) for peer, files in file_index.items()])
    pool.close()
    pool.join()
    peers_with_file = [peer for peer in peers_with_file if peer is not None]

    return jsonify({'peers': peers_with_file}), 200
