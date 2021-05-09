from utils import *

class Cell(object):

    def __init__(self, row, col, domain=-1, is_fixed=False):
        self.row = row
        self.col = col
        # blocks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.b = get_block_index(row, col)
        if domain == -1 and not is_fixed:
            self.domain = set_all_bits(9)
        else:
            self.domain = domain
        self.is_fixed = is_fixed

    def set_domain(self, domain):
        self.domain = domain
        
    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)

