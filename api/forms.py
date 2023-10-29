from django import forms

turmas = [[turma.split(",")[0], turma.split(",")[1].title(), turma.split(",")[2]] for turma in open("turmas.txt", 'r').readlines()]

class ClassroomsForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=[(i, f"{turmas[i][0]} | {turmas[i][1]} | {turmas[i][2]}") for i in range(len(turmas))],
        widget=forms.CheckboxSelectMultiple,
    )
