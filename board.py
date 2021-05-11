from cell import Cell
from utils import *
from priority_queue import *
import copy

class Board(object):

    def __init__(self, board, rules=[False, False, False, False, False, False]):
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
        self.queue = PriorityQueue()
        self.domains = {}
        self.neighbors = {}
        self.rules = rules
        self.num_backtracks = 0
        
        for cell in self.cells:
            if not cell.is_fixed:
                domain = self.get_domain(cell.row, cell.col)
                self.domains[(cell.row, cell.col)] = domain
                entry = Entry(count_set_bits(domain), cell)
                self.queue.push(entry)
                self.populate_neighbors(cell)
                        
    def populate_neighbors(self, cell):
        self.neighbors[(cell.row, cell.col)] = []
        for c in range(len(self.board[cell.row])):
            if self.board[cell.row][c] == '0' and c != cell.col:
                self.neighbors[(cell.row, cell.col)].append((cell.row, c))
        
        for r in range(len(self.board)):
            if self.board[r][cell.col] == '0' and r != cell.row:
                self.neighbors[(cell.row, cell.col)].append((r, cell.col))
                
        (rs, cs) = get_cells_from_block(cell.b)
        list_block_neighbors = [(r,c) for c in cs for r in rs if self.board[r][c] == '0' and r != cell.row and c != cell.col]
        self.neighbors[(cell.row, cell.col)].extend(list_block_neighbors)
            
        
    def get_domain(self, row, col):
        row_remaining = flip_all(self.rows[row])
        col_remaining = flip_all(self.cols[col])
        block_remaining = flip_all(self.blocks[get_block_index(row, col)])
        remaining = get_intersection_set(row_remaining, col_remaining, block_remaining)
        return remaining
        
    def solve_simple_backtracking(self):
        if self.expandedNodes >= 1000:
            print("could not solve")
            print("Searches: ", self.expandedNodes)
            print("Number of backtracks: ", self.num_backtracks)
            return False

        location = self.get_next_location()
        if location[0] == -1:
            print("solved")
            self.printB()
            return True
        else:
            self.expandedNodes += 1
            choices = list(map(int, bits_to_string(location[2])))
            for choice in choices:
                # self.printB()
                if self.is_safe(location[0],location[1],choice):
                    self.board[location[0]][location[1]] = str(choice)
                    self.rows[location[0]] = set_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = set_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = set_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
                    # self.printB()
                    cell = self.cells[get_cell_index(location[0], location[1])]
                    assignments = copy.deepcopy(self.domains)
                    neighbors = self.neighbors[(location[0], location[1])]
                    backup_domains = copy.deepcopy(self.domains)
                    if self.forward_checking(cell, set_bit(0, choice - 1), assignments, neighbors):
                        self.domains = assignments
                        if self.solve_simple_backtracking():
                            return True
                    self.domains = backup_domains
                    self.board[location[0]][location[1]] = '0'
                    self.rows[location[0]] = reset_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = reset_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = reset_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
                    self.num_backtracks += 1
            return False
        
    def solve_most_constraint_backtracking(self):
        if self.expandedNodes >= 1000:
            print("could not solve")
            print("Searches: ", self.expandedNodes)
            print("Number of backtracks: ", self.num_backtracks)
            return False

        location = self.get_next_location_MRV()
        if location[0] == -1:
            print("Solved")
            self.printB()
            return True
        else:
            self.expandedNodes += 1
            for choice in list(map(int, bits_to_string(location[2]))):
                if self.is_safe(location[0],location[1],choice):
                    self.board[location[0]][location[1]] = str(choice)
                    self.rows[location[0]] = set_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = set_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = set_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
                    # self.printB()
                    cell = self.cells[get_cell_index(location[0], location[1])]
                    assignments = copy.deepcopy(self.domains)
                    neighbors = self.neighbors[(location[0], location[1])]
                    backup_domains = copy.deepcopy(self.domains)
                    if self.forward_checking(cell, set_bit(0, choice - 1), assignments, neighbors):
                        self.domains = assignments
                        if self.solve_simple_backtracking():
                            return True
                    self.domains = backup_domains
                    self.board[location[0]][location[1]] = '0'
                    self.rows[location[0]] = reset_bit(self.rows[location[0]], choice - 1)
                    self.cols[location[1]] = reset_bit(self.cols[location[1]], choice - 1)
                    self.blocks[get_block_index(location[0], location[1])] = reset_bit(self.blocks[get_block_index(location[0], location[1])], choice - 1)
                    self.num_backtracks += 1
            return False
        
    def forward_checking(self, cell, choice, assignments, neighbors):
        assignments[(cell.row, cell.col)] = choice
        for neighbor in neighbors:
            if assignments[neighbor] & choice == 0:
                continue
            assignments[neighbor] = assignments[neighbor] ^ choice
            remaining = assignments[neighbor]
            neighbor_cell = self.cells[get_cell_index(neighbor[0], neighbor[1])]
            if count_set_bits(remaining) == 0:
                return False
            elif self.rules[0] and count_set_bits(remaining) == 1:
                # naked singles
                if not self.forward_checking(neighbor_cell, remaining, assignments, self.neighbors[neighbor]):
                    return False
            else:
                self.inference(neighbor_cell, remaining, assignments, self.neighbors[neighbor])
        return True
    
    def inference(self, cell, remaining, assignments, neighbors):
        if self.rules[1] and self.hidden_n_tuples(cell, remaining, assignments, neighbors, 1):
            return True
        elif self.rules[2] and self.naked_ns(cell, remaining, assignments, neighbors, 2):
            return True
        elif self.rules[3] and self.hidden_n_tuples(cell, remaining, assignments, neighbors, 2):
            return True
        elif self.rules[4] and self.naked_ns(cell, remaining, assignments, neighbors, 3):
            return True
        elif self.rules[5] and self.hidden_n_tuples(cell, remaining, assignments, neighbors, 3):
            return True   
        return False
    
    def naked_ns(self, cell, remaining, assignments, neighbors, n):
        if count_set_bits(remaining) == n:
            result = {"row": [(cell.row, cell.col)], "col": [(cell.row, cell.col)], "block": [(cell.row, cell.col)]}
            for neighbor in neighbors:
                n_domain = assignments[neighbor]
                if neighbor[0] == cell.row and remaining == n_domain:
                    result["row"].append(neighbor)
                elif neighbor[1] == cell.col and remaining == n_domain:
                    result["col"].append(neighbor)
                elif neighbor[0] in get_cells_from_block(cell.b)[0] and neighbor[1] in get_cells_from_block(cell.b)[1] and remaining == n_domain:
                    result["block"].append(neighbor)
            
            if len(result["row"]) == n:
                for neighbor in neighbors:
                    if neighbor[0] == cell.row and neighbor not in result["row"]:
                        assignments[neighbor] = (~remaining & 511) & (assignments[neighbor] ^ remaining)
                return True
            elif len(result["col"]) == n:
                for neighbor in neighbors:
                    if neighbor[1] == cell.col and neighbor not in result["col"]:
                        assignments[neighbor] = (~remaining & 511) & (assignments[neighbor] ^ remaining)
                return True
            elif len(result["block"]) == n:
                for neighbor in neighbors:
                    if neighbor[0] in get_cells_from_block(cell.b)[0] and neighbor[1] in get_cells_from_block(cell.b)[1] and neighbor not in result["block"]:
                        assignments[neighbor] = (~remaining & 511) & (assignments[neighbor] ^ remaining)
                return True
        return False
                
    
    def hidden_n_tuples(self, cell, cell_domain, assignments, neighbors, n):
        hidden_ns_row = 0
        hidden_ns_col = 0
        hidden_ns_block = 0
        if n == 1:
            hidden_ns_row = cell_domain
            hidden_ns_col = cell_domain
            hidden_ns_block = cell_domain
        result = {"row": {}, "col": {}, "block": {}}
        for neighbor in neighbors:
            n_domain = assignments[neighbor]
            if n > 1:
                if neighbor[0] == cell.row:
                    hidden_ns_row = cell_domain & n_domain
                elif neighbor[1] == cell.col:
                    hidden_ns_col = cell_domain & n_domain
                elif neighbor[0] in get_cells_from_block(cell.b)[0] and neighbor[1] in get_cells_from_block(cell.b)[1]:
                    hidden_ns_block = cell_domain & n_domain
                    
                if count_set_bits(hidden_ns_row) == n:
                    if not hidden_ns_row in result["row"].keys():
                        result["row"][hidden_ns_row] = []
                    result["row"][hidden_ns_row].append(neighbor)
                    hidden_ns_row = 0
                elif count_set_bits(hidden_ns_col) == n:
                    if not hidden_ns_col in result["col"].keys():
                        result["row"][hidden_ns_col] = []
                    result["row"][hidden_ns_col].append(neighbor)
                    hidden_ns_col = 0
                elif count_set_bits(hidden_ns_block) == n:
                    if not hidden_ns_block in result["block"].keys():
                        result["row"][hidden_ns_block] = []
                    result["row"][hidden_ns_block].append(neighbor)
                    hidden_ns_block = 0
            else:
                if neighbor[0] == cell.row:
                    hidden_ns_row = (~n_domain & 511) & (hidden_ns_row ^ n_domain)
                elif neighbor[1] == cell.col:
                    hidden_ns_col = (~n_domain & 511) & (hidden_ns_col ^ n_domain)
                elif neighbor[0] in get_cells_from_block(cell.b)[0] and neighbor[1] in get_cells_from_block(cell.b)[1]:
                    hidden_ns_block = (~n_domain & 511) & (hidden_ns_block ^ n_domain)
        flag = False       
        if n == 1:
            if count_set_bits(hidden_ns_row) == 1:
                for square in result["row"]:
                    assignments[square] = hidden_ns_row
                flag = True
            elif count_set_bits(hidden_ns_col) == 1:
                for square in result["col"]:
                    assignments[square] = hidden_ns_col
                flag = True
            elif count_set_bits(hidden_ns_block) == 1:
                for square in result["block"]:
                    assignments[square] = hidden_ns_block
                flag = True
        else:
            
            for key in result["row"]:
                if len(result["row"][key]) == n:
                    for square in result["row"][key]:
                        assignments[square] = key
                    flag = True
            for key in result["col"]:
                if len(result["col"][key]) == n:
                    for square in result["col"][key]:
                        assignments[square] = key
                    flag = True
            for key in result["block"]:
                if len(result["block"][key]) == n:
                    for square in result["block"][key]:
                        assignments[square] = key
                    flag = True
        
        return flag
            

    def get_next_location(self):    
        for cell in self.cells:
            if self.board[cell.row][cell.col] == '0':
                domain = self.domains[(cell.row, cell.col)]
                return (cell.row, cell.col, domain)
        return (-1, -1)

    def get_next_location_MRV(self):
        # update the domain lengths first
        new_q = PriorityQueue()
        while not self.queue.is_empty():
            entry = self.queue.pop()
            entry.domain_length = count_set_bits(self.domains[(entry.cell.row, entry.cell.col)])
            new_q.push(entry)
        self.queue = new_q    
        
        if not self.queue.is_empty():
            entry = self.queue.pop()
            cell = entry.cell
            domain = self.domains[(cell.row, cell.col)]
            return (cell.row, cell.col, domain)
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
        # print("Domains: ")
        # for i in self.domains.keys():
        #     print(str(i) + ": ", bits_to_string(self.domains[i]))
        for r in self.board:
            print(r)
        print("Searches: ", self.expandedNodes)
        print("Number of backtracks: ", self.num_backtracks)

            
