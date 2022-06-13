import os
import re

import requests

DEFAULT_DST_FOLDER = os.getcwd()


def download(source: str, destination: str = DEFAULT_DST_FOLDER) -> str:
    name_file = source.split('//')[-1]
    name_local = '{0}{1}'.format(re.sub(r'\W', '-', name_file), '.html')
    request = requests.get(source, stream=True)
    with open(os.path.join(destination, name_local), 'wb') as filename:
        for chunk in request.iter_content():
            filename.write(chunk)

    return os.path.join(destination, name_local)
