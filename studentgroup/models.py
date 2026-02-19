# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

CLASS_CHOICES = [
    ('1', 'First Year'),
    ('2', 'Second Year'),
    ('3', 'Third Year'),
    ('4', 'Fourth Year'),
]

PROGRAM_CHOICES = [
    ('BTECH_CS', 'BTech CS'),
    ('BTECH_CS_DS', 'BTech CS-DS'),
    ('BTECH_CE', 'BTech CE'),
    ('BTECH_IT', 'BTech IT'),
    ('BTECH_AIML', 'BTech AIML'),
    ('MBA_TECH_CE', 'MBATech CE'),
]


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def is_full(self):
        return self.student_count() >= 10


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sap_id = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=1, choices=CLASS_CHOICES)
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="students"
    )

    def clean(self):
        if self.teacher.is_full():
            raise ValidationError("This teacher already has 10 students.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
