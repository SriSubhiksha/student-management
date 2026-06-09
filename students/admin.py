from django.contrib import admin

from .models import Student,MailTemplate

admin.site.register(Student)
admin.site.register(MailTemplate)