from django.shortcuts import render
from .forms import ClassroomsForm
from .util import interval_scheduling, Turma
from django.db.models import Q


def lerTurmas():
    return [Turma(turma.split(",")[0], turma.split(",")[1], turma.split(",")[2]) for turma in open("turmas.txt", 'r').readlines()]


def index(request):
    turmas = lerTurmas()
    filtered_turmas = turmas
    if request.method == 'POST':
        form = ClassroomsForm(request.POST)
        search_text = request.POST.get('search', None)
        if search_text:
            filtered_turmas = [turma for turma in turmas if search_text.lower() in turma.nome.lower() or search_text.lower() in turma.professor.lower()]
            filtered_choices = [(i, f"{filtered_turmas[i].nome} | {filtered_turmas[i].professor.title()} | {filtered_turmas[i].horario}") for i in range(len(filtered_turmas))]
            form.fields["choices"].choices = filtered_choices
        if request.POST.get('limpar', None):
            form = ClassroomsForm()
            form.fields["search"].initial = ''
        if form.is_valid():
            selected_choices = form.cleaned_data['choices']
            resultado = interval_scheduling([turmas[int(i)] for i in selected_choices])
            return render(request, 'api/index.html', {'form': form, 'resultado': resultado})
    else:
        form = ClassroomsForm()
    return render(request, 'api/index.html', {'form': form})

