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
    def get_all_moves(self, board):
        return [['B', (4, 5)]]


if __name__ == '__main__':
    test = OthelloBot(8)
    print(test.make_move())
