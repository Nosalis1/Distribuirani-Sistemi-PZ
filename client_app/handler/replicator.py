from functools import wraps
import os
import requests


def replicator(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        from . import distributed_files, CONFIGURATION

        files = [file for file in distributed_files if file.file_last_modified != os.path.getmtime(
            f'{CONFIGURATION.SHARED_DIR}/{file.file_name}')]
        for file in files:
            file.file_last_modified = os.path.getmtime(f'{CONFIGURATION.SHARED_DIR}/{file.file_name}')
            response = requests.post(f'{CONFIGURATION.SERVER_ADDRESS}/replicate',
                                     json={'owner': CONFIGURATION.PORT, 'filename': file.file_name})
            if response.status_code == 200:
                print("Successfully replicated file")
            else:
                print("Failed to replicate file")
        return func(*args, **kwargs)

    return decorated_function
