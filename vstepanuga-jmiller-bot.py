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

    def make_move(self, x, y, color='W'):
        if self.is_valid_move(x, y, color):
            temp_board = list(tuple(self.board))
            temp_board[x][y] = color
            cost = self.evaluate_board_cost(temp_board)
            return [cost, temp_board]

    def is_valid_move(self, x, y, color):
        return True

    def evaluate_board_cost(self, temp_board):
        return 1


if __name__ == '__main__':
    test = OthelloBot(8)
    print(test.make_move(3, 5))
