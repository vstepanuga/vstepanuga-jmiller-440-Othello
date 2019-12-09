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

if __name__ == '__main__':
    test = OthelloBot(8)
    print(test.board)
