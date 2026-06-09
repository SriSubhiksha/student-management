from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    age = models.IntegerField()
    
    

    def __str__(self):
        return self.name
    

class MailTemplate(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class MailTemplate(models.Model):

    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
from django.db import models


class StudentMarks(models.Model):

    student = models.OneToOneField(
        'Student',
        on_delete=models.CASCADE
    )

    tamil = models.IntegerField()

    english = models.IntegerField()

    maths = models.IntegerField()

    science = models.IntegerField()

    social_science = models.IntegerField()

    total = models.IntegerField(
        default=0
    )

    average = models.FloatField(
        default=0
    )

    def save(self, *args, **kwargs):

        self.total = (
            self.tamil +
            self.english +
            self.maths +
            self.science +
            self.social_science
        )

        self.average = self.total / 5

        super().save(*args, **kwargs)