from django.db import models
from django import forms
from .models import Student, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show only teachers who are NOT full
        self.fields['teacher'].queryset = Teacher.objects.annotate(
            total=models.Count('students')
        ).filter(total__lt=10)
