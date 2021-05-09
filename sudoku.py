import sys
from board import Board

def get_board(cells):
    board = []
    i = 0
    temp = []
    for s in cells:
        if s >= "0" and s <= "9":
            # print(s)
            temp.append(s)
            i = (i + 1) % 9
            if i == 0 and len(temp) != 0:
                board.append(temp)
                temp = []
     
    return board

def print_board(board):
    print()
    for r in board:
        print(r)
    print()
    
    
# board = [['2', '4', '0', '3', '0', '0', '0', '0', '0'],
# ['0', '0', '0', '5', '2', '0', '4', '0', '7'],
# ['0', '0', '0', '0', '4', '6', '0', '0', '8'],
# ['6', '1', '0', '7', '0', '0', '0', '8', '4'],
# ['0', '0', '9', '0', '6', '0', '5', '0', '0'],
# ['7', '3', '0', '0', '0', '5', '0', '6', '1'],
# ['1', '0', '0', '4', '7', '0', '0', '0', '0'],
# ['3', '0', '2', '0', '5', '1', '0', '0', '0'],
# ['0', '0', '0', '0', '0', '2', '0', '1', '9']]

# board_state = Board(board)
# board_state.solve_simple_backtracking()
if __name__ == "__main__":
    input_string = sys.argv[1]
    board = get_board(input_string)
    board_state = Board(board)
    print_board(board)
    # board_state.print()
    
    board_state.solve_simple_backtracking()
    print_board(board_state.board)
