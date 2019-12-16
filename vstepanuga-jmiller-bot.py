import copy
import time
import OthelloEngine


class OthelloBot:
    def __init__(self, color, board_size=8, time_limit=2.0):
        self.global_min = 65
        self.global_max = -1
        self.color = color
        self.time_limit = time_limit
        self.adjacencies = OthelloEngine.get_adjacencies()

    # def initialize_test_board(self, board_size):
    #     self.board = [['-' for j in range(board_size)] for i in range(board_size)]
    #     self.board[1][0] = "W"
    #     self.piece_hash["10"] = "W"
    #     self.board[2][0] = "B"
    #     self.piece_hash["20"] = "B"

    def make_move(self, board, move, piece_hash, real_move=False):
        if move is not None:
            color = move[0]
            x = move[1][0]
            y = move[1][1]

            board[x][y] = color
            if real_move:
                piece_hash[str(x) + str(y)] = color
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
    def get_move(self, board):
        color = self.color
        self.global_min = 65
        self.global_max = -1
        result = self.evaluate_alphabeta_tree(2, board, color, True)
        if result is not None:
            return tuple(self.evaluate_alphabeta_tree(2, board, color, True)[0])
        return None

    # Function for just returning a tree based on the current self.board as well as the color of the player
    def evaluate_alphabeta_tree(self, depth, board, color, you):
        # board = copy.deepcopy(board)
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

            if len(evaluated_moves) > 0:
                if you:
                    return max(evaluated_moves, key=lambda item: item[1])
                else:
                    return min(evaluated_moves, key=lambda item: item[1])

        for move in legal_moves:
            temp_board = copy.deepcopy(board)
            temp_piece_hash = self.build_piece_hash(temp_board)
            self.make_move(temp_board, move, temp_piece_hash, True)

            # Swap the color when going into a deeper depth to change player.
            color = self.color_swap(color)

            temp_move = self.evaluate_alphabeta_tree(depth - 1, temp_board, color, not you)

            # Swap the color when coming back from recursive depth to change player.
            color = self.color_swap(color)

            if temp_move is not None:
                if you:
                    if temp_move[1] > self.global_max:
                        self.global_max = temp_move[1]
                else:
                    if temp_move[1] < self.global_min:
                        self.global_min = temp_move[1]

                if depth is not 2:
                    if you:
                        if temp_move[1] > self.global_min:
                            return temp_move
                    else:
                        if temp_move[1] < self.global_max:
                            return temp_move

                depth_alphabeta_costs.append([move, temp_move[1]])
        if len(depth_alphabeta_costs) > 0:
            if you:
                return max(depth_alphabeta_costs, key=lambda item: item[1])
            else:
                return min(depth_alphabeta_costs, key=lambda item: item[1])
        else:
            return None

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

    def check_win(self, board):
        white_pieces = 0
        black_pieces = 0
        for row in board:
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

    @staticmethod
    def build_piece_hash(board):
        piece_hash = dict()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] != "-":
                    piece_hash[str(row)+str(col)] = board[row][col]
        return piece_hash

    @staticmethod
    def color_swap(color):
        if color == 'W':
            color = 'B'
        else:
            color = 'W'

        return color


if __name__ == '__main__':
    # Create a test board.
    board_size = 8
    board = [['-' for j in range(board_size)] for i in range(board_size)]
    board[3][3] = 'B'
    board[3][4] = 'W'
    board[4][3] = 'W'
    board[4][4] = 'B'

    test = OthelloBot('B')
    player = 'B'
    winner = None

    while winner is None:
        best_move = test.get_move(board)
        print("Color: " + test.color + ' Best move: ' + str(best_move))
        test.make_move(board, best_move, test.build_piece_hash(board))
        if test.color == 'B':
            test.color = 'W'
        else:
            test.color = 'B'
        for i in board:
            print(i)
        print()
        winner = test.check_win(board)
    print(test.check_win(board))
