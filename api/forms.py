from django import forms

class ClassroomsForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
        widget=forms.CheckboxSelectMultiple,
    )
