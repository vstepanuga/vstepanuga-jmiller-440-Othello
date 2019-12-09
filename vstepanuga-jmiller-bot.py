import copy


class OthelloBot:
    def __init__(self, board_size):
        self.board = []
        self.initialize_board(board_size)

    def initialize_board(self, board_size):
        for i in range(board_size):
            temp = []
            for j in range(board_size):
                temp.append('-')
            self.board.append(temp)

    # Function responsible for making the most powerful move in the 2 second span.
    # Returns a move: (Color, (X, Y))
    def make_move(self):
        legal_moves = self.get_all_moves(self.board)
        for move in legal_moves:
            self.evaluate_move(move[1][0], move[1][1], move[0])

    # Function which counts the move cost
    def evaluate_move(self, x, y, color='W'):
        temp_board = copy.deepcopy(self.board)
        temp_board[x][y] = color
        cost = self.evaluate_board_cost(temp_board)
        return [cost, temp_board]

    def is_valid_move(self, x, y, color):
        return True

    def evaluate_board_cost(self, temp_board):
        return 1

    def get_all_moves(self, board):
        return ['B', (4, 5)]


if __name__ == '__main__':
    test = OthelloBot(8)
