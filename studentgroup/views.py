# Create your views here.
import openpyxl
from django.http import HttpResponse
from .models import Student

from django.shortcuts import render, redirect
from .forms import StudentForm
from django.contrib import messages

def student_entry(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submitted successfully!")
            return redirect('student_entry')
    else:
        form = StudentForm()

    return render(request, 'studentgroup/student_form.html', {'form': form})


def export_students_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Student Report"

    headers = [
        "First Name", "Last Name", "SAP ID",
        "Roll Number", "Class", "Program", "Teacher"
    ]
    ws.append(headers)

    students = Student.objects.select_related('teacher').all()

    for student in students:
        ws.append([
            student.first_name,
            student.last_name,
            student.sap_id,
            student.roll_number,
            student.get_student_class_display(),
            student.get_program_display(),
            student.teacher.name
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=student_report.xlsx'
    wb.save(response)
    return response
