import requests
import logging
import base64
import time

import numpy as np
import binascii


import classifier as ML

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

archis = ['alphaev56', 'arm', 'avr', 'm68k', 'mips', 'mipsel', 'powerpc', 's390', 'sh4', 'sparc', 'x86_64', 'xtensa']
if len(archis) != 12:
    print("Incorrect number of architectures!")
    exit(1)


class Server(object):
    url = 'https://mlb.praetorian.com'
    log = logging.getLogger(__name__)

    def __init__(self):
        self.session = requests.session()
        self.binary  = None
        self.hash    = None
        self.wins    = 0
        self.targets = []

    def _request(self, route, method='get', data=None):
        while True:
            try:
                if method == 'get':
                    r = self.session.get(self.url + route)
                else:
                    r = self.session.post(self.url + route, data=data)
                if r.status_code == 429:
                    raise Exception('Rate Limit Exception')
                if r.status_code == 500:
                    raise Exception('Unknown Server Exception')

                return r.json()
            except Exception as e:
                self.log.error(e)
                self.log.info('Waiting 60 seconds before next request')
                time.sleep(60)

    def get(self):
        r = self._request("/challenge")
        self.targets = r.get('target', [])
        self.binary  = base64.b64decode(r.get('binary', ''))
        return r

    def post(self, target):
        r = self._request("/solve", method="post", data={"target": target})
        self.wins = r.get('correct', 0)
        self.hash = r.get('hash', self.hash)
        self.ans  = r.get('target', 'unknown')
        return r

def get_data():
    s = Server()

    map = {}
    for archi in archis:
        map[archi] = []



    for i in range(10 * 12):
        s.get()
        s.post(s.targets[0])
        # hexlify the data
        data = binascii.hexlify(s.binary)
        # nice pythonic way of separating every 4 hex digits (1 32-bit word each)
        data = [data[i:i + 4] for i in range(0, len(data), 4)]
        map[s.ans] += data.copy()

    for name in archis:
        with open(name + ".npy", 'wb+') as f:
            np.save(f, map[name])

    # print(map)


def read_data():
    map = {}
    for name in archis:
        with open(name + ".npy", 'rb') as f:
            map[name] = np.load(f)
            # print(name)
            # print(np.load(f))

    return list(map.values()), list(map.keys())



if __name__ == "__main__":
    import random

    # create the server object
    s = Server()

    for _ in range(10):
        # query the /challenge endpoint
        s.get()
        # print(s.targets)
        # print(s.binary)

        get_data()
        # data, targets = read_data()
        # print(data)


        # for i in range(len(targets)):
            # print(targets[i])
            # print(data[i])

        # classifier = ML.Classifier(s.binary, s.targets)
        # classifier.train()

        # choose a random target and /solve
        target = random.choice(s.targets)
        s.post(target)

        # s.log.info("Guess:[{: >9}]   Answer:[{: >9}]   Wins:[{: >3}]".format(target, s.ans, s.wins))

        # 500 consecutive correct answers are required to win
        # very very unlikely with current code
        if s.hash:
            s.log.info("You win! {}".format(s.hash))