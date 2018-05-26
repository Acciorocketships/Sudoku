############################################################
# CIS 521: Homework 4
############################################################

student_name = "Ryan Kortvelesy"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from Queue import Queue
from copy import deepcopy


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    return [[(row,col) for col in xrange(9)] for row in xrange(9)]

def sudoku_arcs():
    arcs = []
    for row1 in xrange(9):
        for col1 in xrange(9):
            for row2 in xrange(9):
                if row2 != row1:
                    arcs.append( ((row1,col1),(row2,col1)) )
            for col2 in xrange(9):
                if col2 != col1:
                    arcs.append( ((row1,col1),(row1,col2)) )
            for row2 in xrange(3*int(row1/3),3*int(row1/3)+3):
                for col2 in xrange(3*int(col1/3),3*int(col1/3)+3):
                    if (row1 != row2) and (col1 != col2):
                        arcs.append( ((row1,col1),(row2,col2)) )
    return arcs

# Gets all outgoing arcs from cell1 (except (cell1,cell2) if cell2 is given)
def sudoku_arc_neighbors(cell1,cell2=None):
    arcs = []
    for row in xrange(9):
        if (row != cell1[0]) and ((row,cell1[1]) != cell2):
            arcs.append( ((row,cell1[1]),cell1) )
    for col in xrange(9):
        if (col != cell1[1]) and ((cell1[0],col) != cell2):
            arcs.append( ((cell1[0],col),cell1) )
    for row in xrange(3*int(cell1[0]/3),3*int(cell1[0]/3)+3):
        for col in xrange(3*int(cell1[1]/3),3*int(cell1[1]/3)+3):
            if (row != cell1[0]) and (col != cell1[1]) and ((row,col) != cell2):
                arcs.append( ((row,col),cell1) )
    return arcs

# generator that yields the other cells in the same box
def same_box(cell):
    for row in xrange(3*int(cell[0]/3),3*int(cell[0]/3)+3):
        for col in xrange(3*int(cell[1]/3),3*int(cell[1]/3)+3):
            if not (row == cell[0] and col == cell[1]):
                yield (row,col)

# generator that yields the other cells in the same column
def same_col(cell):
    for row in xrange(9):
        if (row != cell[0]):
            yield (row,cell[1])

# generator that yields the other cells in the same row
def same_row(cell):
    for col in xrange(9):
        if (col != cell[1]):
            yield (cell[0],col)


def read_board(path):
    with open(path,"r") as inputfile:
        inputboard = inputfile.readlines()
    board = {}
    for row in xrange(9):
        for col in xrange(9):
            if inputboard[row][col] == '*':
                board[(row,col)] = set([1,2,3,4,5,6,7,8,9])
            else:
                board[(row,col)] = set([int(inputboard[row][col])])
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.step = False
        self.nextcell = None
        self.nextval = None

    def next(self):
        self.step = True
        self.nextcell = None
        self.infer_improved()
        return (self.nextcell,self.nextval)

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1,cell2) in Sudoku.ARCS:
            for value in list(self.board[cell1]):
                if (len(self.board[cell2]) == 1) and (value in self.board[cell2]):
                    self.board[cell1].remove(value)
                    if len(self.board[cell1]) == 1:
                        self.nextcell = cell1
                        self.nextval = list(self.board[cell1])[0]
                    return True
        return False

    def infer_ac3(self):
        arcqueue = Queue()
        for arc in Sudoku.ARCS:
            arcqueue.put_nowait(arc)
        while not arcqueue.empty():
            arc = arcqueue.get()
            if (self.remove_inconsistent_values(arc[0],arc[1])):
                if (self.step) and (self.nextcell != None):
                    return
                for neighbor in sudoku_arc_neighbors(arc[0],arc[1]):
                    arcqueue.put_nowait(neighbor)

    def infer_improved(self):
        self.infer_ac3()
        if (self.step) and (self.nextcell != None):
            return
        while (self.deductions() and ((not self.step) or (self.nextcell == None))):
            self.infer_ac3()
            if (self.step) and (self.nextcell != None):
                return

    # Makes more complex deductions
    # Returns True if it can solve a square, and false if it can't
    # Returns None if there is a contradiction in the board
    def deductions(self):
        madechange = False
        for row in xrange(9):
            for col in xrange(9):
                cell = (row,col)
                values = self.board[cell]
                if len(values) > 1:
                    for value in values:
                        result = self.check_arcs(cell,value)
                        madechange |= result
                        if result:
                            if self.step:
                                return
                            break
                elif len(values) == 0:
                    return None
        return madechange

    # Checks if it can be deduced that a given cell is the only place for a given value,
    # given that the value can't go in any other squares of its row/column/box.
    # If so, it sets that cell to that value and returns True. If not, it returns False.
    def check_arcs(self,cell,value):
        # Check Box
        valuepresent = False
        for othercell in same_box(cell):
            if value in self.board[othercell]:
                valuepresent = True
                break
        if not valuepresent:
            self.board[cell] = set([value])
            self.nextcell = cell
            self.nextval = value
            return True
        # Check Row
        valuepresent = False
        for othercell in same_row(cell):
            if value in self.board[othercell]:
                valuepresent = True
                break
        if not valuepresent:
            self.board[cell] = set([value])
            self.nextcell = cell
            self.nextval = value
            return True
        # Check Column
        valuepresent = False
        for othercell in same_col(cell):
            if value in self.board[othercell]:
                valuepresent = True
                break
        if not valuepresent:
            self.board[cell] = set([value])
            self.nextcell = cell
            self.nextval = value
            return True
        return False


    def infer_with_guessing(self):
        stored = []
        choice = []
        cell = []
        result = True
        while True:
            while (result): # Attempt to solve
                self.infer_ac3() # Repeatedly check all normal constraints available then make all deductions available
                result = self.deductions() # Run until we have checked normal constraints but can't make any deductions
            if (result == None): # There was a contradiction
                if choice[-1] == len(stored[-1][cell[-1]]): # None of the guesses at this level work. The guess at the last level must be wrong. Go back.
                    choice.pop()
                    cell.pop()
                    stored.pop()
                self.board = deepcopy(stored[-1]) # Restore the last working board
            else: # No contradiction yet, but it got stuck. Make another guess
                choice.append(0)
                cell.append(self.unsolved_cell()) # gets unsolved cell with the smallest number of possibilities.
                if (cell[-1] == None): # If the board is solved, return
                    return
                stored.append(deepcopy(self.board)) # Store current board in case the guess doesn't work
            values = list(self.board[cell[-1]]); values.sort()
            value = values[choice[-1] % len(self.board[cell[-1]])] # Choose a value from the set of possibilities
            self.board[cell[-1]] = set([value]) # test out that value
            choice[-1] += 1 # Increments the index of the "randomly" chosen value to not pick the same one twice
            result = True


    # Returns unsolved cell with the smallest number of possibilities.
    # Returns None if solved.
    def unsolved_cell(self):
        smallest = float("inf")
        cell = None
        for row in xrange(9):
            for col in xrange(9):
                size = len(self.board[(row,col)])
                if (size > 1) and (size < smallest):
                    smallest = size
                    cell = (row,col)
        return cell


    def print_board(self):
        for row in xrange(9):
            for col in xrange(9):
                if len(self.board[(row,col)]) == 1:
                    print "[" + str(list(self.board[(row,col)])[0]) + "]",
                elif len(self.board[(row,col)]) == 0:
                    print "Board Contains Contradiction"
                    return
                else:
                    print "[ ]",
                if (col == 2) or (col == 5):
                    print "|",
            if (row == 2) or (row == 5):
                print " "
                print "--------------------------------------",
            print " "

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
6 hours.
"""

feedback_question_2 = """
Infer with guessing was by far the most difficult part. It took me a while to figure out
that you often don't catch that a guess is incorrect until several guesses into the future.
It was a bit challenging to find a way to keep track of which element we are currently on in each
layer of the guess 'stack', and how to go back to that. I also had some problems with doing a normal copy
instead of a deep copy, which caused aliasing issues.
"""

feedback_question_3 = """
Although it was the most challenging part, I quite liked the infer with guessing problem, because it made me think.
The only thing I would change about the assignment is to add more information about how to test it.
"""
