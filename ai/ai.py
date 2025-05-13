from core.data_manager import DataManager

DEPTH = 1
# Generate all possible moves, and then all these possibles moves


"""
Pieces value :
1 - no value
2 - 9
3 - 1
4 - 3
5 - 3
6 - 5
"""

pieces_values = {
    "1": 0,
    "2": 9,
    "3": 1,
    "4": 3,
    "5": 3,
    "6": 5
}


def evaluate_board(board, player_color):
    """
    Evaluate the board position for a color
    """
    total = 0
    for row in board:
        for column in row:
            if column is None:
                continue
            type = column[0]
            color = column[1]

            value = pieces_values[type]
            if color != player_color:
                value = -value
            total += value
    return total
                

class Ai:
    def __init__(self, datamanager: DataManager):
        self.datamas = datamanager
    
    @staticmethod
    def get_pieces(board, color):
        positions = []
        for y in range(8):
            for x in range(8):
                cell = board[y][x]
                if cell is not None and cell[1] == color:
                    positions.append((x, y))
        return positions
    
    def get_best_move(self, max_depth=3):
        player_color = self.datamas.color  # Couleur du joueur courant (ex: 'w' ou 'b')
        to_color = {
            "w": "b",
            "b": "w"
        }

        def minimax(board, depth, maximizing_player):
            current_color = self.datamas.color if maximizing_player else to_color[self.datamas.color]
            best_score = float('-inf') if maximizing_player else float('inf')
            best_move = None

            # Obtenir toutes les pièces du joueur courant
            positions = self.get_pieces(board, current_color)

            for pos in positions:
                moves = self.datamas.get_possible_positions(pos, ennemy=not maximizing_player)
                for move in moves:
                    # Crée un nouveau plateau avec le mouvement appliqué
                    new_board = [row[:] for row in board]
                    piece = new_board[pos[1]][pos[0]]
                    new_board[move[1]][move[0]] = piece
                    new_board[pos[1]][pos[0]] = None

                    if depth == 1:
                        score = evaluate_board(new_board, player_color)
                    else:
                        score, _ = minimax(new_board, depth - 1, not maximizing_player)

                    # Maximiser ou minimiser selon le joueur
                    if maximizing_player and score > best_score:
                        best_score = score
                        best_move = (pos, move)
                    elif not maximizing_player and score < best_score:
                        best_score = score
                        best_move = (pos, move)

            return best_score, best_move

        _, best_move = minimax(self.datamas.chessboard, max_depth, maximizing_player=True)
        return best_move


