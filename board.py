from cell import Cell
from utils import *

class Board(object):

    def __init__(self, board):
        self.board = board
        self.cells = []
        self.rows = [0] * 9
        self.cols = [0] * 9
        self.blocks = [0] * 9
        self.expandedNodes = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == "0":
                    self.cells.append(Cell(i, j))
                else:
                    board_int = int(board[i][j]) - 1
                    self.rows[i] = set_bit(self.rows[i], board_int)
                    self.cols[j] = set_bit(self.cols[j], board_int)
                    self.blocks[get_block_index(i, j)] = set_bit(self.blocks[get_block_index(i, j)], board_int)
                    self.cells.append(Cell(i, j, is_fixed=True))
        # self.current = self.cells[0]

    def solve_simple_backtracking(self):
        if self.expandedNodes >= 999999:
            return False

        location = self.get_next_location()
        if location[0] == -1:
            self.printB()
            return True
        else:
            self.expandedNodes += 1
            for choice in range(1, 10):
                if self.is_safe(location[0],location[1],choice):
                    self.board[location[0]][location[1]] = str(choice)
                    self.rows[location[0]] = set_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = set_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = set_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
                    self.printB()
                    if self.solve_simple_backtracking():
                        return True
                    self.board[location[0]][location[1]] = '0'
                    self.rows[location[0]] = reset_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = reset_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = reset_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
            return False

    def get_next_location(self):    
        for cell in self.cells:
            if self.board[cell.row][cell.col] == '0':
                return (cell.row, cell.col)
        return (-1, -1)

    def is_safe(self, row, col, choice):
        return not test_bit(self.rows[row], choice - 1) and not test_bit(self.cols[col], choice - 1) and not test_bit(self.blocks[get_block_index(row, col)], choice - 1)

    def printB(self):
        # print("Rows:")
        # for i in range(len(self.rows)):
        #     print(str(i + 1) + ": ", bits_to_string(self.rows[i]))
        # print("\nCols:")
        # for i in range(len(self.cols)):
        #     print(str(i + 1) + ": ", bits_to_string(self.cols[i]))
        # print("\nBlocks:")
        # for i in range(len(self.blocks)):
        #     print(str(i + 1) + ": ", bits_to_string(self.blocks[i]))
            
        print()
        for r in self.board:
            print(r)
        print()
        print(self.expandedNodes)

            
