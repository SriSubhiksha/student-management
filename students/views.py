from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from .models import MailTemplate
from .models import Student
from .forms import MailTemplateForm
from .forms import StudentForm
from .models import StudentMarks
from .forms import StudentMarksForm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors

from .models import StudentMarks

# Student List + Filter Search
def student_list(request):

    students = Student.objects.all()

    student_id = request.GET.get('student_id')
    name = request.GET.get('name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    age = request.GET.get('age')
    course = request.GET.get('course')

    if student_id:
        students = students.filter(
            student_id__icontains=student_id
        )

    if name:
        students = students.filter(
            name__icontains=name
        )

    if email:
        students = students.filter(
            email__icontains=email
        )

    if phone:
        students = students.filter(
            phone__icontains=phone
        )

    if age:
        students = students.filter(
            age=age
        )

    if course:
        students = students.filter(
            course__icontains=course
        )

    return render(
        request,
        'students/student_list.html',
        {
            'students': students
        }
    )


# Add Student
def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            request.session['student_data'] = request.POST.dict()

            if 'edit_id' in request.session:
                del request.session['edit_id']

            return redirect('confirm_student')

    else:
        form = StudentForm()


    return render(
        request,
        'students/student_form.html',
        {
            'form': form
        }
    )



def export_students_excel(request):

    wb = Workbook()
    ws = wb.active

    ws.append([
        'Student ID',
        'Name',
        'Email',
        'Phone',
        'Age',
        'Course'
    ])

    students = Student.objects.all()

    for student in students:

        ws.append([
            student.student_id,
            student.name,
            student.email,
            student.phone,
            student.age,
            student.course
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=students.xlsx'
    )

    wb.save(response)

    return response

# Edit Student
def edit_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            request.session['student_data'] = request.POST.dict()
            request.session['edit_id'] = pk

            return redirect('confirm_student')

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'students/student_form.html',
        {
            'form': form
        }
    )


# Confirm Save Page
def confirm_student(request):

    data = request.session.get('student_data')

    if not data:
        return redirect('student_list')

    if request.method == 'POST':

        edit_id = request.session.get('edit_id')

        if edit_id:

            student = Student.objects.get(id=edit_id)

            form = StudentForm(
                data,
                instance=student
            )

            if form.is_valid():
                form.save()

            del request.session['edit_id']

            messages.success(
                request,
                "Student Updated Successfully!"
            )

        else:

            form = StudentForm(data)

            if form.is_valid():
                form.save()

            messages.success(
                request,
                "Student Saved Successfully!"
            )

        del request.session['student_data']

        return redirect('student_list')

    return render(
        request,
        'students/confirm_student.html',
        {
            'data': data
        }
    )


#MailTemplate.objects.create(
    title="Holiday Notice",
    subject="Holiday Notice",
    body="Dear Student,\n\nTomorrow is declared as a holiday.\n\nRegards,\nABC "
#)

#MailTemplate.objects.create(
    title="Fee Reminder",
    subject="Fee Reminder",
    body="Dear Student,\n\nPlease pay your fees before the due date.\n\nRegards,\nABC School"
#)

#MailTemplate.objects.create(
    title="Attendance Alert",
    subject="Attendance Alert",
    body="Dear Student,\n\nYour attendance percentage is low.\n\nRegards,\nABC School"
#)

#MailTemplate.objects.create(
    title="Examination Notice",
    subject="Examination Notice",
    body="Dear Student,\n\nExaminations will commence shortly.\n\nRegards,\nABC School"
#)

# Student Details
def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        'students/student_detail.html',
        {
            'student': student
        }
    )

def mail_templates(request):

    templates = MailTemplate.objects.all()

    return render(
        request,
        'students/mail_templates.html',
        {
            'templates': templates
        }
    )

def set_active_template(request, pk):

    MailTemplate.objects.update(
        is_active=False
    )

    template = MailTemplate.objects.get(
        id=pk
    )

    template.is_active = True
    template.save()

    messages.success(
         request,
        "Mail template selected successfully."
    )

    return redirect(
        'mail_templates'
    )

def reset_mail_templates(request):

    MailTemplate.objects.all().update(
        is_active=False
    )

    messages.success(
        request,
        "Mail template reset successfully."
    )

    return redirect(
        'mail_templates'
    )

# Delete Student
def delete_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    student.delete()

    messages.success(
        request,
        "Student Deleted Successfully!"
    )

    return redirect(
        'student_list'
    )


# Send Mail
def send_student_mail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    active_template = MailTemplate.objects.filter(
        is_active=True
    ).first()

    if active_template:

        subject = active_template.subject

        message = active_template.body

    else:

        subject = "ABC School "

        message = """
Dear Student,

GOOD DAY!!!
"""

    send_mail(
        subject,
        message,
        'yourgmail@gmail.com',
        [student.email],
        fail_silently=False
    )

    messages.success(
        request,
        f"Mail sent successfully to {student.name}"
    )

    return redirect(
        'student_list'
    )
    
def add_mail_template(request):

    if request.method == 'POST':

        form = MailTemplateForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Mail Template Added Successfully!"
            )

            return redirect(
                'mail_templates'
            )

    else:

        form = MailTemplateForm()

    return render(
        request,
        'students/add_mail_template.html',
        {
            'form': form
        }
    )
def template_detail(request, pk):

    template = get_object_or_404(
        MailTemplate,
        pk=pk
    )

    return render(
        request,
        'students/template_detail.html',
        {
            'template': template
        }
    )
def edit_mail_template(request, pk):

    template = get_object_or_404(
        MailTemplate,
        pk=pk
    )

    if request.method == 'POST':

        form = MailTemplateForm(
            request.POST,
            instance=template
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Mail Template Updated Successfully!"
            )

            return redirect(
                'mail_templates'
            )

    else:

        form = MailTemplateForm(
            instance=template
        )

    return render(
        request,
        'students/edit_mail_template.html',
        {
            'form': form,
            'template': template
        }
    )

def enter_marks(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    marks = StudentMarks.objects.filter(
        student=student
    ).first()

    if request.method == 'POST':

        form = StudentMarksForm(
            request.POST,
            instance=marks
        )

        if form.is_valid():

            request.session['marks_data'] = request.POST.dict()
            request.session['student_id_marks'] = student.id

            return redirect(
                'confirm_marks'
            )

    else:

        form = StudentMarksForm(
            instance=marks
        )

    return render(
        request,
        'students/enter_marks.html',
        {
            'student': student,
            'form': form
        }
    )

def show_marks(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    marks = get_object_or_404(
        StudentMarks,
        student=student
    )

    return render(
        request,
        'students/show_marks.html',
        {
            'student': student,
            'marks': marks
        }
    )
def confirm_marks(request):

    data = request.session.get(
        'marks_data'
    )

    student_id = request.session.get(
        'student_id_marks'
    )

    if not data:
        return redirect(
            'student_list'
        )

    student = Student.objects.get(
        id=student_id
    )

    if request.method == 'POST':

        marks = StudentMarks.objects.filter(
            student=student
        ).first()

        form = StudentMarksForm(
            data,
            instance=marks
        )

        if form.is_valid():

            obj = form.save(
                commit=False
            )

            obj.student = student

            obj.save()

        del request.session['marks_data']
        del request.session['student_id_marks']

        messages.success(
            request,
            "Marks Saved Successfully!"
        )

        return redirect(
            'student_list'
        )

    return render(
        request,
        'students/confirm_marks.html',
        {
            'student': student,
            'data': data
        }
    )
def download_excel(request):

    wb = Workbook()

    ws = wb.active

    ws.title = "Student Report"

    ws.append([

        'Student ID',
        'Name',
        'Email',
        'Phone',
        'Age',
        'Course',

        'Tamil',
        'English',
        'Maths',
        'Science',
        'Social Science',

        'Total',
        'Average'

    ])

    students = Student.objects.all()

    for student in students:

        marks = StudentMarks.objects.filter(
            student=student
        ).first()

        ws.append([

            student.student_id,
            student.name,
            student.email,
            student.phone,
            student.age,
            student.course,

            marks.tamil if marks else '',
            marks.english if marks else '',
            marks.maths if marks else '',
            marks.science if marks else '',
            marks.social_science if marks else '',

            marks.total if marks else '',
            marks.average if marks else ''

        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=student_report.xlsx'

    wb.save(response)

    return response

def download_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=student_report.pdf'

    doc = SimpleDocTemplate(
        response
    )

    data = [[

        'Student ID',
        'Name',
        'Course',

        'Tamil',
        'English',
        'Maths',
        'Science',
        'Social Science',

        'Total',

    ]]

    students = Student.objects.all()

    for student in students:

        marks = StudentMarks.objects.filter(
            student=student
        ).first()

        data.append([

             student.student_id,
            student.name,
            student.course,

            marks.tamil if marks else '',
            marks.english if marks else '',
            marks.maths if marks else '',
            marks.science if marks else '',
            marks.social_science if marks else '',

            marks.total if marks else '',
           

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ('BACKGROUND',
             (0, 0),
             (-1, 0),
             colors.lightgrey),

            ('GRID',
             (0, 0),
             (-1, -1),
             1,
             colors.black)

        ])

    )

    doc.build([table])

    return response