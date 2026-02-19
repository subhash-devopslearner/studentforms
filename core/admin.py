from django.contrib import admin
from .models import AcademicYear, Department, Program, Branch, Semester

# Register your models here.
admin.site.register(AcademicYear)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Branch)
admin.site.register(Semester)