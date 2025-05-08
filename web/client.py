import socket
import threading
import pickle  # Pour sérialiser les données
from discovery import discover_server
import pygame as pg

PORT = 5000

clientx, clienty = (0, 0)

def receive_messages(sock):
    global clientx, clienty  # Référence à la variable globale
    while True:
        try:
            msg = sock.recv(1024)
            if msg:
                # Désérialiser les données reçues
                clientx, clienty = pickle.loads(msg)
            else:
                break
        except:
            break

def main():
    print("🔍 Recherche du serveur...")
    HOST = discover_server()
    if not HOST:
        print("❌ Aucun serveur trouvé.")
        return

    print(f"✅ Serveur trouvé à l'adresse {HOST}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[🟢 Connecté au serveur {HOST}:{PORT}]")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    # Initialisation de pygame
    pg.init()
    display = pg.display.set_mode((400, 400))  # Taille de la fenêtre
    pg.display.set_caption("Client side")
    posx, posy = 50, 50  # Position initiale
    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            posy -= 10
        if keys[pg.K_DOWN]:
            posy += 10
        if keys[pg.K_LEFT]:
            posx -= 10
        if keys[pg.K_RIGHT]:
            posx += 10

        # Sérialiser et envoyer les coordonnées
        msg = pickle.dumps((posx, posy))
        client.send(msg)

        # Dessiner les éléments
        display.fill((255, 255, 255))  # Remplir l'écran de blanc
        pg.draw.rect(display, (0, 255, 0), pg.Rect(posx, posy, 20, 20))  # Carré vert (mouvement local)
        pg.draw.rect(display, (255, 0, 0), pg.Rect(clientx, clienty, 20, 20))  # Carré rouge (mouvement distant)

        pg.display.update()
        clock.tick(30)

    client.close()
    print("[🔴 Déconnecté]")

if __name__ == "__main__":
    main()
