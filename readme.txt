Python 3.8
libraries:
    sys, heapq, copy

command:
    python sudoku.py input.txt <algorithm> <inference rules> > out.txt

algorithms:
        0 -> simple
        1 -> MCV
inferences:
        0 -> no inferences
        1 -> naked and hidden singles
        2 -> naked and hidden singles, doubles
        3 -> naked and hidden singles, doubles, and triples