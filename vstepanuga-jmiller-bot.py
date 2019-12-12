import copy
import time
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

    def make_move(self, board, move, real_move=False):
        if move is not None:
            color = move[0]
            x = move[1][0]
            y = move[1][1]

            board[x][y] = color
            for adjacency in self.adjacencies:
                self.make_move_helper(board, x, y, adjacency[0], adjacency[1], color, real_move)

    def make_move_helper(self, child_board, x, y, x_offset, y_offset, color, real_move):
        temp_list = []
        while not self.illegal_position(x + x_offset, y + y_offset) and child_board[x + x_offset][y + y_offset] != color \
                and child_board[x + x_offset][y + y_offset] != '-':
            temp_list.append((child_board[x + x_offset][y + y_offset], (x+x_offset, y+y_offset)))
            x += x_offset
            y += y_offset
        if not self.illegal_position(x + x_offset, y + y_offset) and child_board[x + x_offset][y + y_offset] == color:
            self.list_swap(child_board, temp_list, real_move)

    @staticmethod
    def illegal_position(x, y):
        return x < 0 or x > 7 or y < 0 or y > 7

    def list_swap(self, child_board, swap_list, real_move):
        if len(swap_list) > 0:
            for move in swap_list:
                color = move[0]
                x = move[1][0]
                y = move[1][1]
                if color == 'W':
                    child_board[x][y] = 'B'
                    if real_move:
                        self.piece_hash[str(x) + str(y)] = 'B'
                else:
                    child_board[x][y] = 'W'
                    if real_move:
                        self.piece_hash[str(x) + str(y)] = 'W'

    # Function responsible for making the most powerful move in the 2 second span.
    # Returns a move: (Color, (X, Y))
    def get_move(self, board, color):
        self.board = board
        legal_moves = self.get_all_moves(color)
        print("Legal Moves: ", legal_moves)
        if len(legal_moves) == 0:
            return None
        evaluated_moves = []

        for move in legal_moves:
            evaluated_moves.append([move, self.evaluate_move(move)])

        return tuple(max(evaluated_moves, key=lambda item: item[1])[0])

    # Function which counts the move cost
    def evaluate_move(self, move):
        temp_board = copy.deepcopy(self.board)
        self.make_move(temp_board, move)
        cost = self.evaluate_board_cost(temp_board, move[0])
        return cost

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
                    if not self.illegal_position(x + adjacency[0], y + adjacency[1]) and \
                            OthelloEngine.is_valid_move(x + adjacency[0], y + adjacency[1],
                                                        -adjacency[0], -adjacency[1], self.board, color, False):
                        moves.append([color, (x + adjacency[0], y + adjacency[1])])
        return moves

    def check_win(self):
        white_pieces = 0
        black_pieces = 0
        for row in self.board:
            for col in row:
                if col == "-":
                    return None
                if col == "W":
                    white_pieces += 1
                else:
                    black_pieces += 1
        if white_pieces > black_pieces:
            return "White is the winner"
        elif black_pieces > white_pieces:
            return "Black is the winner"
        else:
            return "It's a tie"


if __name__ == '__main__':
    test = OthelloBot()
    player = "B"
    winner = None
    counter = 0
    while winner is None and counter < 10:
        best_move = test.get_move(test.board, player)
        test.make_move(test.board, best_move, True)
        if player == "B":
            player = "W"
        else:
            player = "B"
        for i in test.board:
            print(i)
        print()
        winner = test.check_win()
        counter += 1
    print(test.check_win())
