from core.renderer import Renderer
from core.cst_manager import CstManager
from core.data_manager import DataManager
from core.input_manager import *
import socket
from web.server_ip_discover import discover_server
from core.audio_manager import MixerPlay
from widgets.widget_manager import *
from ai.ai import Ai

def main():

    cst_manager = CstManager()
    input_manager = InputManager(cst_manager)
    data_manager = DataManager()
    renderer = Renderer(cst_manager)
    # Menu render
    menu_shown = True
    widget_manager = WidgetManager(MENU_WIDGETS, renderer)
    while menu_shown:
        mouse_pos = input_manager.get_mouse_pos()
        events = input_manager.get_pg_events()
        if LEFTCLICK in events:
            return_value = widget_manager.on_click()
            if return_value:
                menu_shown = False
        if QUIT in events:
            menu_shown = False
            return
        widget_manager.update(mouse_pos)
        widget_manager.update_widget_surfaces()
        renderer.render_menu(widget_manager.widgets)
        renderer.update_display()

    # Debug
    def debug_log(message):
        name = "white" if data_manager.color == "w" else "black"
        print(f"[Client {name}] : {message}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = discover_server()
    client.connect((server_ip, 9999))
    client.send("[from client : connected to server]".encode())
    print("Serveur answer :", client.recv(1024).decode())
    if client.recv(1024).decode() == "AI?":
        print("sending the data")
        client.send(str(return_value["ai"]).encode())

    fullscreen = False

    client.settimeout(0.01)
    is_playing = False
    is_ai = False
    running = True
    while running:
        try:
            message = client.recv(1024).decode()
            if message.startswith("YOU_ARE_COLOR"):
                data_manager.setup_board(message)
                renderer.set_window_title(f"Client {message[14:]}")
                client.send("AKN".encode())
                debug_log("Received color data")
            if message == "YOU_AI":
                is_ai = True
                ia = Ai(data_manager)
                client.send("AKN".encode())
            if message.startswith("YOU_ARE_PLAYING"):
                debug_log("Currently on play")
                is_playing = True
                pos1, pos2 = data_manager.from_message_decode_opponent_pos(message)
                data_manager.movepiece(pos1, pos2)
                renderer.setup_opponent_animation(pos1, pos2, data_manager.get_at(pos2))
                data_manager.get_check_data()
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
            
        if is_ai and is_playing:
            move = ia.get_best_move(1)
            selected, release = move
            data_manager.movepiece(selected, release)
            data_manager.get_check_data()
            if release != selected: # If piece stays at the same place
                if data_manager.check_data:
                    debug_log(f"color in checkmate position by {data_manager.check_data}")
                client.send(f"{selected}-{release}".encode())
                debug_log("I sent the data")
                is_playing = False
                MixerPlay(1)

        if LEFTCLICK in events and LEFTCLICK not in input_manager.last_events and is_playing:
            # Grab piece
            grabpos =cst_manager.get_gridpos(events[LEFTCLICK])
            if data_manager.get_color_at(grabpos) == data_manager.color:
                data_manager.selected_piece_pos = grabpos
                data_manager.set_possible_positions()
        if LEFTCLICK_RELEASE in events and LEFTCLICK_RELEASE not in input_manager.last_events and data_manager.selected_piece_pos and is_playing:
            release_position = cst_manager.get_gridpos(events[LEFTCLICK_RELEASE])
            if data_manager.check_move_validity(data_manager.selected_piece_pos, release_position, debug=True):
                data_manager.movepiece(data_manager.selected_piece_pos, release_position)
                data_manager.get_check_data()
                if release_position != data_manager.selected_piece_pos: # If piece stays at the same place
                    if data_manager.check_data:
                        debug_log(f"color in checkmate position by {data_manager.check_data}")
                    client.send(f"{data_manager.selected_piece_pos}-{release_position}".encode())
                    debug_log("I sent the data")
                    is_playing = False
                    MixerPlay(1)
            # If the move is valid or not, these statements hold true
            data_manager.selected_piece_pos = None
            data_manager.possible_moves = []

        input_manager.last_events = events
        
        renderer.render_on_screen(data_manager, input_manager.get_mouse_pos())
        renderer.update_display()


if __name__ =="__main__":
    main()

# Jouer ou non avec un timer
# check echec et mat

# POssibility to add very bad ai (1-2 steps ahead)
# Multiplayer
# Movable pieces
# les blancs et les noirs sont en bas -> mirror les moves de l'autre
# Ajotuer des sons
# Grab les pièces
# Fignoler avec choix ou non le l'ia
# Debug quand un pion bouffe de 2 cases



# Possiblement + tard :
# Ajouter + de 2 parties en simultané
# Possibilité de choisir les textures de ses pièces dans menu
# POssibilité de choisir la couleur du bg menu