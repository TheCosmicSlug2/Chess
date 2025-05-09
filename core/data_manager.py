"""
Pieces :
0 : blank
roi : 1
reine : 2
pion : 3
fou : 4
chevalier : 5
tour : 6
"""
from ast import literal_eval

def intfloat_div(nb, div):
    if nb%div == 0:
        return nb // div
    return nb / div

class DataManager:
    def __init__(self):
        self.chessboard = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, "6b", "1b", None],
            [None, None, None, None, None, None, "6b", None],
            [None, None, None, None, "2b", None, None, None],
            [None, None, None, "2w", None, None, None, None],
            [None, "6w", None, None, None, None, None, None],
            [None, "1w", "6w", None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        self.selected_piece_pos = None
        self.check_data = {"w": None, "b": None}
        self.color = None
        self.possible_moves = []
    
    def get_at(self, gripos) -> str | None:
        return self.chessboard[gripos[1]][gripos[0]]

    def get_color_at(self, gridpos):
        value = self.get_at(gridpos)
        if value is None:
            return None
        return value[1]
    
    def get_piece_type_at(self, gridpos):
        value = self.get_at(gridpos)
        if value is None:
            return None
        return value[0]

    def set_at(self, gridpos, value) -> None:
        self.chessboard[gridpos[1]][gridpos[0]] = value

    def print_board(self):
        for row in self.chessboard:
            print("-----" * len(row) + "-")
            for column in row:
                content = "  " if column is None else column
                print(f"| {content} ", end="")
            print("|")
        print("-----" * len(row) + "-")
    
    def setup_board(self, message):
        chessboard = [
            ["6b", "5b", "4b", "2b", "1b", "4b", "5b", "6b"],
            ["3b" for _ in range(8)],
            *[[None for _ in range(8)] for _ in range(4)],
            ["3w" for _ in range(8)],
            ["6w", "5w", "4w", "2w", "1w", "4w", "5w", "6w"],
        ]

        if message == "YOU_ARE_COLOR_WHITE":
            self.chessboard = chessboard
            self.color = "w"
        if message == "YOU_ARE_COLOR_BLACK":
            self.chessboard = list(reversed(chessboard))
            self.chessboard[0] = list(reversed(self.chessboard[0]))
            self.chessboard[7] = list(reversed(self.chessboard[7]))
            self.color = "b"
        self.print_board()

    
    def movepiece(self, startpos, endpos):
        piece_name = self.get_at(startpos)
        self.set_at(startpos, None)
        self.set_at(endpos, piece_name)
    
    def check_move_validity(self, startpos, endpos, debug=False):
        startx, starty = startpos
        endx, endy = endpos
        piece = self.get_at(startpos)
        endcell_color = self.get_color_at(endpos)
        piece_type = piece[0]
        piece_color = piece[1]
        
        d_mov = (endx - startx, endy - starty)
        if d_mov == (0, 0):
            return True

        pieces_movement = {
            "1": [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)],
            "2": [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)],
            "4": [(-1, -1), (1, -1), (-1, 1), (1, 1)],
            "5": [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, -1), (-2, 1)],
            "6": [(0, -1), (-1, 0), (1, 0), (0, 1)]
        }

        def fast_piece_check(type):
            max_d = max(abs(d_mov[0]), abs(d_mov[1]))
            vec_move = (intfloat_div(d_mov[0], max_d), intfloat_div(d_mov[1], max_d))
            if vec_move not in pieces_movement[type]:
                return False
            for cell_dst in range(1, max_d):
                mov = (vec_move[0] * cell_dst, vec_move[1] * cell_dst)
                if self.chessboard[starty + mov[1]][startx + mov[0]]: # Check if there are pieces in the path
                    return False
            if endcell_color == piece_color: # Check if last if own piece
                return False
            return True                

        if piece_type == "1":
            if d_mov not in pieces_movement["1"]:
                return False
            if endcell_color == piece_color: # Check ovewrites his own pieces
                return False
        if piece_type == "2" and not fast_piece_check("2"):
            return False
        if piece_type == "3":
            if d_mov not in [(1, -1), (-1, -1), (0, -2), (0, -1)]:
                return False
            if d_mov in [(1, -1), (-1, -1)]:
                if endcell_color is None or endcell_color == self.color:
                    return False
            if d_mov == (0, -2) and starty != 6:
                return False
            if d_mov == (0, -1) and endcell_color != None:
                return False
        if piece_type == "4" and not fast_piece_check('4'):
            return False
        if piece_type == "5":
            if d_mov not in pieces_movement["5"]:
                return False
            if endcell_color == piece_color:
                return False
        if piece_type == "6" and not fast_piece_check("6"):
            return False
        
        return True

    def set_possible_positions(self):
        self.possible_moves = []
        for row in range(8):
            for column in range(8):
                if self.check_move_validity(self.selected_piece_pos, (column, row)):
                    self.possible_moves.append((column, row))

    def get_check_data(self):
        for color in ("w", "b"):
            self.check_data[color] = self.check_for_checkmate(color)
        return self.check_data
    
    def from_message_decode_opponent_pos(self, message):
        if message == "YOU_ARE_PLAYING":
            return None
        name, startpos, endpos = message.split("-")

        startpos, endpos = literal_eval(startpos), literal_eval(endpos)
        changed_startpos = (7 - startpos[0], 7 - startpos[1])
        changed_endpos = (7 - endpos[0], 7 - endpos[1])
        return changed_startpos, changed_endpos
    
    def check_for_checkmate(self, color):
        # find king and attacking pieces
        anticolor = {
            "w": "b",
            "b": "w"
        }
        attacking = []
        for row_idx, row in enumerate(self.chessboard):
            for col_idx, col in enumerate(row):
                if col is None:
                    continue
                if col == "1" + color:
                    king_pos = (col_idx, row_idx)
                if col[1] == anticolor[color]:
                    attacking.append((col_idx, row_idx))
        
        for attacking_pos in attacking:
            if self.check_move_validity(attacking_pos, king_pos):
                return (king_pos, attacking_pos)
        return None