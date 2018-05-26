import sudokusolver as solver
import code

sudoku = solver.Sudoku(solver.read_board("puzzle.txt"))

def disp():
	sudoku.print_board()

def stepsolve():
	cell,value = sudoku.next()
	print str(value) + " in cell " + str((cell[0]+1,cell[1]+1))

def step():
	cell,value = sudoku.next()
	print_with_mark(cell)
	print "cell " + str((cell[0]+1,cell[1]+1))

def solve():
    sudoku.step = False
    sudoku.infer_with_guessing()
    disp()


def print_with_mark(cell):
    for row in xrange(9):
        for col in xrange(9):
       	    if (row,col) == cell:
                print " X ",
            elif len(sudoku.board[(row,col)]) == 1:
                print "[" + str(list(sudoku.board[(row,col)])[0]) + "]",
            elif len(sudoku.board[(row,col)]) == 0:
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

if __name__ == '__main__':
	code.interact(local=locals())




