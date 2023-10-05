from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TestNotes

# class NotesUpdateForm(forms.ModelForm):
#     class Meta:
#         model = TestNotes
#         fields = ['brief', 'description']