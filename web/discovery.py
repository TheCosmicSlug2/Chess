# discovery.py
import socket
import threading

DISCOVERY_PORT = 6000
DISCOVERY_MESSAGE = "who_is_there"
RESPONSE_MESSAGE = "i_am_here"

def start_discovery_server():
    def listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", DISCOVERY_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            if data.decode() == DISCOVERY_MESSAGE:
                sock.sendto(RESPONSE_MESSAGE.encode(), addr)
    threading.Thread(target=listen, daemon=True).start()

def discover_server(timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    sock.sendto(DISCOVERY_MESSAGE.encode(), ("<broadcast>", DISCOVERY_PORT))
    try:
        data, addr = sock.recvfrom(1024)
        if data.decode() == RESPONSE_MESSAGE:
            return addr[0]
    except socket.timeout:
        return None
