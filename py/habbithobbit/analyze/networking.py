import subprocess
import logging
import socket
import re
import time
import os


def serverAddress():
    if os.environ.get('LOCALHOST_NETWORKING', 0):
        return "127.0.0.1"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 1000))
        return sock.getsockname()[0]
    finally:
        sock.close()


def waitForTCPServer(endpoint, timeout=3, interval=0.05):
    if isinstance(endpoint, int):
        endpoint = ("localhost", endpoint)
    before = time.time()
    while True:
        time.sleep(interval)
        sock = socket.socket()
        try:
            sock.connect(endpoint)
            return
        except:
            pass
        finally:
            sock.close()
        if time.time() - before > timeout:
            raise Exception("TCP server did not answer within timeout")
