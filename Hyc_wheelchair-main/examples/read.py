
from __future__ import print_function

import sys
import time
from gattlib import GATTRequester, GATTResponse


class AsyncReader(object):
    def __init__(self, address):
        self.requester = GATTRequester("40:06:A0:97:74:A9", False)
        self.response = GATTResponse()

        self.connect()
        self.request_data()
        self.wait_response()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

    def request_data(self):
        self.requester.read_by_handle_async(0x12, self.response)

    def wait_response(self):
        while not self.response.received():
            time.sleep(0.1)

        data = self.response.received()[0]

        print("bytes received:", end=' ')
        for b in data:
            print(hex(ord(b)), end=' ')
        print("")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    AsyncReader(sys.argv[1])
    print("Done.")
