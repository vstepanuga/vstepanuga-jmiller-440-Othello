import copy

import OthelloEngine


class OthelloBot:
    def __init__(self):
        self.board = []
        self.piece_hash = dict()
        self.initialize_board(8)
        # self.initialize_test_board(8)
        self.adjacencies = OthelloEngine.get_adjacencies()

    # def initialize_test_board(self, board_size):
    #     self.board = [['-' for j in range(board_size)] for i in range(board_size)]
    #     self.board[1][0] = "W"
    #     self.piece_hash["10"] = "W"
    #     self.board[2][0] = "B"
    #     self.piece_hash["20"] = "B"

    def initialize_board(self, board_size):
        self.board = [['-' for j in range(board_size)] for i in range(board_size)]
        self.board[3][3] = 'B'
        self.board[3][4] = 'W'
        self.board[4][3] = 'W'
        self.board[4][4] = 'B'
        self.piece_hash['33'] = 'B'
        self.piece_hash['34'] = 'W'
        self.piece_hash['43'] = 'W'
        self.piece_hash['44'] = 'B'

    def make_move_helper(self, x, y, x_offset, y_offset, color):
        while self.board[x + x_offset][y + y_offset] != color and self.board[x + x_offset][y + y_offset] != '-' \
                and not self.legal_position(x + x_offset, y + y_offset):
            if self.board[x + x_offset][y + y_offset] == 'W':
                self.board[x + x_offset][y + y_offset] = 'B'
                self.piece_hash[str(x + x_offset) + str(y + y_offset)] = 'B'
            else:
                self.board[x + x_offset][y + y_offset] = 'W'
                self.piece_hash[str(x + x_offset) + str(y + y_offset)] = 'W'
            x += x_offset
            y += y_offset

    @staticmethod
    def legal_position(x, y):
        return x < 0 or x > 7 or y < 0 or y > 7

    def make_move(self, color):
        move = self.get_move(color)
        if move is not None:
            x = move[1][0]
            y = move[1][1]

            self.board[x][y] = color
            for adjacency in self.adjacencies:
                self.make_move_helper(x, y, adjacency[0], adjacency[1], color)

    # Function responsible for making the most powerful move in the 2 second span.
    # Returns a move: (Color, (X, Y))
    def get_move(self, color):
        legal_moves = self.get_all_moves(color)
        if len(legal_moves) == 0:
            return None
        evaluated_moves = []

        for move in legal_moves:
            evaluated_moves.append([move, self.evaluate_move(move[1][0], move[1][1], move[0])])

        if len(legal_moves) > 0:
            return tuple(max(evaluated_moves, key=lambda item: item[0])[0])
        else:
            return

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
            if self.piece_hash[piece] != color:
                x = int(piece[0])
                y = int(piece[1])
                for adjacency in self.adjacencies:
                    if OthelloEngine.is_valid_move(x + adjacency[0], y + adjacency[1], -adjacency[0], -adjacency[1],
                                                   self.board, color, False):
                        moves.append([color, (x + adjacency[0], y + adjacency[1])])
        return moves


if __name__ == '__main__':
    test = OthelloBot()

    for i in test.board:
        print(i)

    print()

    print(test.get_all_moves("B"))
    test.make_move("B")

    for i in test.board:
        print(i)

    print()
    test.make_move("W")

    for i in test.board:
        print(i)

    print()
    test.make_move("B")

    for i in test.board:
        print(i)

    print()
    test.make_move("W")

    for i in test.board:
        print(i)
