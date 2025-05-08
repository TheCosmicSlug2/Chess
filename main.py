from renderer import Renderer
from cst_manager import CstManager
from data_manager import DataManager
from input_manager import *
import socket
from web.server_ip_discover import discover_server

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = discover_server()
    client.connect((server_ip, 9999))
    client.send("[from client : connected to server]".encode())
    print("Serveur answer :", client.recv(1024).decode())

    cst_manager = CstManager()
    input_manager = InputManager(cst_manager)
    data_manager = DataManager()
    renderer = Renderer(cst_manager)
    fullscreen = False


    client.settimeout(0.1)  # Timeout de 1 seconde
    is_playing = False
    running = True
    while running:
        try:
            message = client.recv(1024).decode()
            if message.startswith("YOU_ARE_PLAYING"):
                print("I am playing")
                data_manager.process_opponent_play(message)
                is_playing = True
        except:
            pass
        events = input_manager.get_pg_events()
        if QUIT in events:
            running = False
        if VIDEORESIZE in events:
            cst_manager.update_screen_dimensions(events[VIDEORESIZE], CTRL in events)
            renderer.resize_display()
            renderer.load_textures()
        if F in events and F not in input_manager.last_events:
            fullscreen = not fullscreen
            if fullscreen:
                renderer.go_fullscreen()
                cst_manager.go_fullscreen(renderer.get_fullscreen_dims())
            else:
                cst_manager.update_screen_dimensions(cst_manager.old_dims_mem)
                renderer.resize_display()
            renderer.load_textures()
        if LEFTCLICK in events and LEFTCLICK not in input_manager.last_events and is_playing:
            pos = events[LEFTCLICK]
            gridpos = (pos[0] // cst_manager.cell_width, pos[1] // cst_manager.cell_height)
            if data_manager.selected_piece:
                if data_manager.check_move_validity(data_manager.selected_piece, gridpos):
                    data_manager.movepiece(data_manager.selected_piece, gridpos)
                    check_pos = data_manager.get_checkmate_data()
                    if check_pos:
                        print(f"color in checkmate position by {check_pos}")
                    client.send(f"{data_manager.selected_piece}-{gridpos}".encode())
                    print("I sent the data")
                    data_manager.selected_piece = None
                    is_playing = False
            elif data_manager.get_at(gridpos) != None:
                data_manager.selected_piece = gridpos
        
        input_manager.last_events = events
        
        renderer.render_on_screen(data_manager)
        renderer.update_display()


if __name__ =="__main__":
    main()

# Movable pieces
# Multiplayer
# POssibility to add very bad ai (1-2 steps ahead)