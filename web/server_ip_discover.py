# discovery_client.py
import socket

def discover_server(timeout=5, port=9998):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    message = "DISCOVER_SERVER".encode()
    broadcast_address = ('<broadcast>', port)

    try:
        sock.sendto(message, broadcast_address)
        print("[ Broadcast send, looking for servers...]")
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "SERVER_HERE":
            print(f"[ Serveur trouvé à {server_addr[0]}]")
            return server_addr[0]
    except socket.timeout:
        print("[ No server answer ]")
        return None
    finally:
        sock.close()
