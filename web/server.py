import socket
import threading
from discovery import start_discovery_server
import pygame as pg
import pickle  # Utilisé pour sérialiser les tuples avant de les envoyer

HOST = '0.0.0.0'
PORT = 5000

otherx, othery = (0, 0)

def receive_messages(conn):
    global otherx, othery
    while True:
        try:
            # Réception des données
            msg = conn.recv(1024)
            if msg:
                # Désérialiser le message reçu (un tuple)
                otherx, othery = pickle.loads(msg)
            else:
                break
        except Exception as e:
            print(e)
            break

def main():
    start_discovery_server()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[🟢 Serveur en attente de connexion sur le port {PORT}]")

    conn, addr = server.accept()
    print(f"[✅ Connecté avec le client {addr}]")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    # Initialisation de pygame
    pg.init()
    display = pg.display.set_mode((400, 400))  # Taille de la fenêtre
    pg.display.set_caption("Server side")
    posx, posy = 100, 100  # Position du carré vert
    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                posx, posy = pg.mouse.get_pos()

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            posy -= 1
        if keys[pg.K_DOWN]:
            posy += 1
        if keys[pg.K_LEFT]:
            posx -= 1
        if keys[pg.K_RIGHT]:
            posx += 1

        # Sérialiser et envoyer les coordonnées
        msg = pickle.dumps((posx, posy))
        conn.send(msg)

        # Dessiner les éléments
        display.fill((255, 255, 255))  # Remplir l'écran de blanc
        pg.draw.rect(display, (0, 255, 0), pg.Rect(posx, posy, 20, 20))  # Carré vert (mouvement local)
        pg.draw.rect(display, (255, 0, 0), pg.Rect(otherx, othery, 20, 20))  # Carré rouge (mouvement distant)

        pg.display.update()  # Mettre à jour l'écran
        clock.tick(30)

    conn.close()
    server.close()
    print("[🔴 Déconnecté]")

if __name__ == "__main__":
    main()
