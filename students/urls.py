from django.urls import path
from . import views

urlpatterns = [

    # Student List
    path(
        '',
        views.student_list,
        name='student_list'
    ),

    # Add Student
    path(
        'add/',
        views.add_student,
        name='add_student'
    ),

    # Edit Student
    path(
        'edit/<int:pk>/',
        views.edit_student,
        name='edit_student'
    ),

    # Delete Student
    path(
        'delete/<int:pk>/',
        views.delete_student,
        name='delete_student'
    ),

    # Student Details
    path(
        'student/<int:pk>/',
        views.student_detail,
        name='student_detail'
    ),

    path(
         'export-excel/',
         views.export_students_excel,
         name='export_students_excel'
    ),
    path(
          'download-pdf/',
         views.download_pdf,
         name='download_pdf'
    ),

    path(
          'download-excel/',
         views.download_excel,
        name='download_excel'
    ),


    # Send Mail
    path(
        'send-mail/<int:pk>/',
        views.send_student_mail,
        name='send_student_mail'
    ),

    path(
    'confirm-student/',
    views.confirm_student,
    name='confirm_student'
),

path(
    'mail-templates/',
    views.mail_templates,
    name='mail_templates'
),

path(
    'set-template/<int:pk>/',
    views.set_active_template,
    name='set_active_template'
),

path(
    'reset-mail/',
    views.reset_mail_templates,
    name='reset_mail_templates'
),
path(
    'add-template/',
    views.add_mail_template,
    name='add_mail_template'
),

path(
    'template/<int:pk>/',
    views.template_detail,
    name='template_detail'
),
path(
    'edit-template/<int:pk>/',
    views.edit_mail_template,
    name='edit_mail_template'
),

path(
    'enter-marks/<int:pk>/',
    views.enter_marks,
    name='enter_marks'
),

path(
    'show-marks/<int:pk>/',
    views.show_marks,
    name='show_marks'
),
path(
    'confirm-marks/',
    views.confirm_marks,
    name='confirm_marks'
),

]