# serveur.py
import socket
import threading

def discovery_responder(port=9998):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    print("[Discover Server actif sur UDP]")
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode() == "DISCOVER_SERVER":
                print(f"[Demande de {addr}]")
                sock.sendto("SERVER_HERE".encode(), addr)
        except:
            continue

def get_response(player):
    while True:
        data = player.recv(1024).decode() # Wait 
        if data:
            return

def main():
    # Lancer le serveur UDP dans un thread séparé
    threading.Thread(target=discovery_responder, daemon=True).start()

    # Lancer le serveur TCP principal
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(2)
    print("[TCP server ready on port 9999]")
    client_list = []

    while len(client_list) < 2:
        client, addr = server.accept()
        client_list.append(client)
        print(client_list)
        print(f"[Connexion of {addr}]")
        print(client.recv(1024).decode())
        client.send("[From server : got your connection]".encode())
    

    server_running = True
    player1 = client_list[0]
    player2 = client_list[1]
    player1.send("YOU_ARE_COLOR_WHITE".encode())
    print("I send YOU_ARE_COLOR_WHITE")
    get_response(player1)
    player2.send("YOU_ARE_COLOR_BLACK".encode())
    
    print("I send YOU_ARE_COLOR_BLACK")
    get_response(player2)
    player1.send("YOU_ARE_PLAYING".encode())
    
    print("I send YOU_ARE_PLAYING")
    while server_running:
        print("[Serveur] En attente du mouvement de", "Joueur 1" if player1 == client_list[0] else "Joueur 2")
        move_data = player1.recv(1024).decode()
        print("[Serveur] Données reçues :", move_data)
        if move_data:
            player1, player2 = player2, player1
            player1.send(f"YOU_ARE_PLAYING-{move_data}".encode())

if __name__ == "__main__":
    main()
