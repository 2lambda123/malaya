import requests
import json
import argparse
import pickle
import os
import time
import random
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='filename')
args = parser.parse_args()
filename = args.filename
retry = 3


class Pointer:
    def __init__(self, filename):
        self.filename = filename
        self.index = 0

    def _save(self):
        with open(self.filename, 'wb') as fopen:
            pickle.dump(self.index, fopen)

    def increment(self):
        self.index += 1
        self._save()

    def load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'rb') as fopen:
            self.index = pickle.load(fopen)


pointer = Pointer(f'{filename}.pickle')
pointer.load()

file = open(f'{filename}.requested', 'a')

with open(filename) as fopen:
    for i, l in tqdm(enumerate(fopen)):
        if i >= pointer.index:
            data = json.loads(l)
            text = data['normalized']
            k = 0
            while True:
                try:
                    r = requests.post('http://localhost:8999/api', timeout=5, json={
                        'text': text,
                        'from': 'ms',
                        'to': 'en',
                        'lite': True,
                    })
                    r = r.json()
                    break
                except Exception as e:
                    print(k, e)
                    
                time.sleep(2)
                k += 1
                
            data = {'src': data, 'r': r}

            d = json.dumps(data)
            file.write(f'{d}\n')
            file.flush()

            pointer.index = i
            pointer._save()

            time.sleep(random.uniform(0.2, 0.5))

file.close()
