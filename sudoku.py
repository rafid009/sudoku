import sys
import time
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
    
def get_boards (file_name):
    f = open(file_name, "r")
    f_lines = f.read().split('\n')
    boards = [] #list of boards, each element is a tuple (no_and_difficulty : string, board : 2D_list)

    i = 0
    lim = len(f_lines)-11

    while (i<=lim):
        list_2d = []
        for j in range(1,10):
            sub = list(f_lines[i+j].strip())
            sub.pop(3)
            sub.pop(6)
            list_2d.append(sub)
        boards.append((f_lines[i].strip() , list_2d))
        i+=11
    return boards

def get_current_time_in_millis():
    return int(time.time() * 1000)

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("invalid input")
        sys.exit(0)
    rules = [False, False, False, False, False, False]
    boards = get_boards(sys.argv[1])
    i = 1
    solved = 0
    for item in boards:
        difficulty = item[0].split()[1]
        board = item[1]
        board_state = None
        # inferences:
        # 0 -> no inferences
        # 1 -> naked and hidden singles
        # 2 -> naked and hidden singles, doubles
        # 3 -> naked and hidden singles, doubles, and triples
        if int(sys.argv[3]) == 1:
            rules[0] = True
            rules[1] = True
        elif int(sys.argv[3]) == 2:
            rules[0] = True
            rules[1] = True
            rules[2] = True
            rules[3] = True
        elif int(sys.argv[3]) == 3:
            rules[0] = True
            rules[1] = True
            rules[2] = True
            rules[3] = True
            rules[4] = True
            rules[5] = True
        print("difficulty: ", difficulty)
        board_state = Board(board, rules)
        start = get_current_time_in_millis()
        # algorithms:
        #     1 -> MCV
        #     0 -> simple
        if int(sys.argv[2]) == 1:          
            if board_state.solve_most_constraint_backtracking():
                solved += 1
            else:
                print("could not solve")
                print("Searches: ", board_state.expandedNodes)
                print("Number of backtracks: ", board_state.num_backtracks)
        else:
            if board_state.solve_simple_backtracking():
                solved += 1
            else:
                print("could not solve")
                print("Searches: ", board_state.expandedNodes)
                print("Number of backtracks: ", board_state.num_backtracks)
        end = get_current_time_in_millis()
        print("Time taken: ", (end - start), " ms")
        print("\n")
        i += 1
        
    print("solved ", solved, " out of ", i, " puzzles")
