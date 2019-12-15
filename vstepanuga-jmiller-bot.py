import copy
import time
import OthelloEngine


class OthelloBot:
    def __init__(self):
        self.board = []
        self.global_min = 65
        self.global_max = -1
        self.color = 'W'
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

    def make_move(self, board, move, piece_hash, real_move=False):
        if move is not None:
            color = move[0]
            x = move[1][0]
            y = move[1][1]

            board[x][y] = color
            for adjacency in self.adjacencies:
                self.make_move_helper(board, x, y, adjacency[0], adjacency[1], piece_hash, color, real_move)

    def make_move_helper(self, child_board, x, y, x_offset, y_offset, piece_hash, color, real_move):
        temp_list = []
        while not self.illegal_position(x + x_offset, y + y_offset) and child_board[x + x_offset][y + y_offset] != color \
                and child_board[x + x_offset][y + y_offset] != '-':
            temp_list.append((child_board[x + x_offset][y + y_offset], (x + x_offset, y + y_offset)))
            x += x_offset
            y += y_offset
        if not self.illegal_position(x + x_offset, y + y_offset) and child_board[x + x_offset][y + y_offset] == color:
            self.list_swap(child_board, temp_list, piece_hash, real_move)

    @staticmethod
    def illegal_position(x, y):
        return x < 0 or x > 7 or y < 0 or y > 7

    def list_swap(self, child_board, swap_list, piece_hash, real_move):
        if len(swap_list) > 0:
            for move in swap_list:
                color = move[0]
                x = move[1][0]
                y = move[1][1]
                if color == 'W':
                    child_board[x][y] = 'B'
                    if real_move:
                        piece_hash[str(x) + str(y)] = 'B'
                else:
                    child_board[x][y] = 'W'
                    if real_move:
                        piece_hash[str(x) + str(y)] = 'W'

    # Function responsible for making the most powerful move in the 2 second span.
    # Returns a move: (Color, (X, Y))
    def get_move(self, board, color):
        self.global_min = 65
        self.global_max = -1
        return self.evaluate_alphabeta_tree(3, board, color, True)

    # Function for just returning a tree based on the current self.board as well as the color of the player
    def evaluate_alphabeta_tree(self, depth, board, color, you):
        board = copy.deepcopy(board)
        piece_hash = self.build_piece_hash(board)

        legal_moves = self.get_all_moves(board, piece_hash, color)
        move_set = set(tuple(move) for move in legal_moves)
        legal_moves = [list(move) for move in move_set]

        depth_alphabeta_costs = []

        # Base Case:
        if depth == 0:
            evaluated_moves = []

            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                evaluated_moves.append([move, self.evaluate_move(temp_board, piece_hash, move)])

            if you:
                return max(evaluated_moves, key=lambda item: item[1])
            else:
                return min(evaluated_moves, key=lambda item: item[1])

        for move in legal_moves:
            self.make_move(board, move, piece_hash, True)

            if color == 'W':
                color = 'B'
            else:
                color = 'W'

            temp_move = self.evaluate_alphabeta_tree(depth - 1, board, color, not you)

            if color == 'W':
                color = 'B'
            else:
                color = 'W'

            if you:
                if temp_move[1] < self.global_max:
                    return temp_move

                depth_alphabeta_costs.append(temp_move)
            else:
                if temp_move[0] > self.global_min:
                    return temp_move
                depth_alphabeta_costs.append(temp_move)

        if you:
            return max(depth_alphabeta_costs, key=lambda item: item[1])
        else:
            return min(depth_alphabeta_costs, key=lambda item: item[1])

    # Function which counts the move cost
    def evaluate_move(self, board, piece_hash, move):
        self.make_move(board, move, piece_hash, False)
        cost = self.evaluate_board_cost(board)
        return cost

    # This function assumes temp_board is already set up with all the correct pieces according to game logic,
    # ready for processing
    def evaluate_board_cost(self, board):
        cost = 0
        for row in board:
            for tile in row:
                if tile is self.color:
                    cost += 1
        return cost

    # Returns a list of all legal moves for a given board state
    def get_all_moves(self, board, piece_hash, color):
        moves = []

        for piece in piece_hash:
            if piece_hash[piece] != color:
                x = int(piece[0])
                y = int(piece[1])
                for adjacency in self.adjacencies:
                    if not self.illegal_position(x + adjacency[0], y + adjacency[1]) and \
                            OthelloEngine.is_valid_move(x + adjacency[0], y + adjacency[1],
                                                        -adjacency[0], -adjacency[1], board, color, False):
                        moves.append([color, (x + adjacency[0], y + adjacency[1])])
        return moves

    def build_piece_hash(self, board):
        piece_hash = dict()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] != "-":
                    piece_hash[str(row)+str(col)] = board[row][col]
        return piece_hash

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

    while winner is None:
        best_move = test.get_move(test.board, player)
        if player == "B":
            player = "W"
        else:
            player = "B"
        for i in test.board:
            print(i)
        print()
        winner = test.check_win()
    print(test.check_win())
