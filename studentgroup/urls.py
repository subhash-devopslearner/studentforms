from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_entry, name='student_entry'),
    path('export-excel/', views.export_students_excel, name='export_excel'),
]
