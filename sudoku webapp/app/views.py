import itertools
import re
from django.contrib import messages
from django.shortcuts import render

from .forms import SudokuForm
from sudoku.sudokumaker import SudokuBoard
from sudoku.sudokusolver import Sudoku


sudokuboard = SudokuBoard()
sudokuboard.generate()


def get_cell_attrs(sudokuform,cell):
	idx = cell[0]*9 + cell[1]
	return sudokuform.form[idx].fields['value'].widget.attrs


def home(request):
	action = request.POST.get('action', None)
	suggest = request.GET.get('suggest', False)
	matrix = request.POST.getlist('matrix')

	sudokuform = SudokuForm()

	if action == 'generate':
		matrix = sudokuboard.generate()
	else:
		matrix = sudokuform.get(request)
	sudokuform.set(matrix)

	if action == 'hint':
		solver = Sudoku(matrix)
		cell,value = next(solver)
		widget = get_cell_attrs(sudokuform,cell)
		mid1 = (cell[0] >= 3 and cell[0] <= 5)
		mid2 = (cell[1] >= 3 and cell[1] <= 5)
		if (mid1 or mid2) and not (mid1 and mid2):
			blinktype = 'blink'
		else:
			blinktype = 'blink2'
		widget['class'] += ' animate ' + blinktype
	elif action == 'check':
		solver = Sudoku(sudokuboard.board)
		solver.step = False
		solver.infer_with_guessing()
		solution = solver.get()
		for row in range(9):
			for col in range(9):
				if (matrix[row][col] != None) and (matrix[row][col] != solution[row][col]):
					widget = get_cell_attrs(sudokuform,(row,col))
					widget['class'] += ' textcolor'


	c = {
		'action': action,
		'form': sudokuform.form,
		# Add attribute here, then use it in home.html with {% if boolvar %} <htmlstuff> {% else %} <htmlstuff> {% endif %}
	}
	return render(request, 'home.html', c)
