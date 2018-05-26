# coding: utf-8
# Copyright (c) 2016, Alexandre Syenchuk (alexpirine), 2016

from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _
import itertools

NUMBERS_NB = 9*9

class NumberForm(forms.Form):
    value = forms.IntegerField(min_value=1, max_value=9, required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'maxlength': 1,
        'size': 1,
        'id': False,
    }))

class SudokuValidatingFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        if sum([bool(v['value']) for v in self.cleaned_data]) < 17:
            raise forms.ValidationError(_("Not enough values for solving this sudoku"))

GridForm = formset_factory(
    NumberForm,
    extra=NUMBERS_NB,
    min_num=NUMBERS_NB, max_num=NUMBERS_NB,
    validate_min=True, validate_max=True,
    formset=SudokuValidatingFormSet
)


class SudokuForm:

    def __init__(self,matrix=[[None]*9]*9):
        self.form = None
        self.set(matrix)
        
    def convert(self,matrix):
        return [{'value': v if (type(v)==int and v >= 1 and v <= 9) else None} for k, v in enumerate(itertools.chain.from_iterable(matrix))]

    def set(self,matrix):
        board = self.convert(matrix)
        self.form = GridForm(initial=board)

    def get(self,request):
        mat = request._post
        # board = [i[:] for i in [[None]*9]*9]
        # for i in range(9):
        #     for j in range(9):
        #         if ('form-'+str(i+j*9)+'-value' in mat) and (mat['form-'+str(i+j*9)+'-value'] != ''):
        #             print('i:', i, "j:", j, "idx:", i+9*j, "val:", mat['form-'+str(i+j*9)+'-value'])
        #             board[j][i] = int(mat['form-'+str(i+j*9)+'-value'])
        #         else:
        #             board[j][i] = 0
        board = [[(int(mat['form-'+str(i+j*9)+'-value']) if (('form-'+str(i+j*9)+'-value' in mat) and (mat['form-'+str(i+j*9)+'-value'] != '')) else None) for i in range(9)] for j in range(9)]
        return board
        