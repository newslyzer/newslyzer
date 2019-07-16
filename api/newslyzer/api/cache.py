import tempfile
import shutil
import os.path as path
import urllib.parse
import json

class CacheService:
    def get(self, url):
        cache_file = calculate_path(url)
        if not path.isfile(cache_file):
            return None

        with open(cache_file) as f:
            return ''.join(f.readlines())

    def store(self, url, result):
        response = json.dumps(result).encode("utf-8")

        from_path = None
        to_path = calculate_path(url)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(response)
            from_path = f.name

        print("Save cache to {}".format(to_path))
        shutil.move(from_path, to_path)

def calculate_path(url):
    return path.join('/tmp/cache', urllib.parse.quote_plus(url))
