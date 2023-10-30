from django import forms
from .util import Turma

turmas = [Turma(turma.split(",")[0], turma.split(",")[1], turma.split(",")[2]) for turma in open("turmas.txt", 'r').readlines()]

class ClassroomsForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=[(i, f"{turmas[i].nome} | {turmas[i].professor.title()} | {turmas[i].horario}") for i in range(len(turmas))],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-scroll'}),
        label='',
    )
    limpar = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())