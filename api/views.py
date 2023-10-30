from django.shortcuts import render
from .forms import ClassroomsForm
from .util import interval_scheduling, Turma

turmas = [Turma(turma.split(",")[0], turma.split(",")[1], turma.split(",")[2]) for turma in open("turmas.txt", 'r').readlines()]

def index(request):
    if request.method == 'POST':
        form = ClassroomsForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['limpar']:
                form = ClassroomsForm()
            else:
                selected_choices = form.cleaned_data['choices']
                resultado = interval_scheduling([turmas[int(i)] for i in selected_choices])
                return render(request, 'api/index.html', {'form': form, 'resultado': resultado})
    else: form = ClassroomsForm()
    return render(request, 'api/index.html', {'form': form})