from django.shortcuts import render
from .forms import ClassroomsForm

def index(request):
    if request.method == 'POST':
        form = ClassroomsForm(request.POST)
        if form.is_valid():
            selected_choices = form.cleaned_data['choices']
            print(selected_choices)
    else: form = ClassroomsForm()
    return render(request, 'api/index.html', {'form': form})