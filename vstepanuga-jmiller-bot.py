import copy

import OthelloEngine


class OthelloBot:
    def __init__(self):
        self.board = []
        self.initialize_board(8)
        self.piece_hash = []
        self.adjacencies = OthelloEngine.get_adjacencies()

    def initialize_board(self, board_size):
        self.board = [['-' for j in range(board_size)] for i in range(board_size)]
        self.board[3][3] = 'B'
        self.board[3][4] = 'W'
        self.board[4][3] = 'W'
        self.board[4][4] = 'B'
        self.piece_hash.append(['B', (3, 3)])
        self.piece_hash.append(['W', (3, 4)])
        self.piece_hash.append(['W', (4, 3)])
        self.piece_hash.append(['B', (4, 4)])

    # Function responsible for making the most powerful move in the 2 second span.
    # Returns a move: (Color, (X, Y))
    def get_move(self):
        legal_moves = self.get_all_moves('W')
        evaluated_moves = []

        for move in legal_moves:
            evaluated_moves.append([move, self.evaluate_move(move[1][0], move[1][1], move[0])])

        return tuple(max(evaluated_moves, key=lambda item: item[0])[0])

    # Function which counts the move cost
    def evaluate_move(self, x, y, color='W'):
        temp_board = copy.deepcopy(self.board)
        temp_board[x][y] = color
        cost = self.evaluate_board_cost(temp_board, color)
        return cost

    def is_valid_move(self, x, y, color):
        return True

    # This function assumes temp_board is already set up with all the correct pieces according to game logic,
    # ready for processing
    @staticmethod
    def evaluate_board_cost(temp_board, color):
        cost = 0
        for row in temp_board:
            for tile in row:
                if tile is color:
                    cost += 1

        return cost

    # Returns a list of all legal moves for a given board state
    def get_all_moves(self, color):
        moves = []

        for piece in self.piece_hash:
            if piece[0] != color:
                x = piece[1][0]
                y = piece[1][1]
                for adjacency in self.adjacencies:
                    if OthelloEngine.is_valid_move(x, y, adjacency[0], adjacency[1], self.board, color, False):
                        moves.append([color, (x, y)])

        return moves


if __name__ == '__main__':
    test = OthelloBot()
    print(test.get_move())
