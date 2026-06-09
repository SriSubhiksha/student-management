from django import forms
from .models import Student
from .models import MailTemplate
import re

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student ID',
                'required': True
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Name',
                'required': True,
                'pattern': '[A-Za-z ]+',
                'title': 'Name should contain alphabets only'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email Address',
                'required': True
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10 Digit Mobile Number',
                'required': True,
                'pattern': '[0-9]{10}',
                'maxlength': '10',
                'title': 'Phone number must contain exactly 10 digits'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Age',
                'required': True,
                'min': '1',
                'max': '80'
            }),

            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Name',
                'required': True
            }),

        }

class MailTemplateForm(forms.ModelForm):

    class Meta:

        model = MailTemplate

        fields = [
            'title',
            'subject',
            'body'
        ]

        widgets = {

            'body': forms.Textarea(
                attrs={
                    'rows':8
                }
            )

        }

from django import forms
from .models import StudentMarks


class StudentMarksForm(forms.ModelForm):

    class Meta:

        model = StudentMarks

        fields = [

            'tamil',
            'english',
            'maths',
            'science',
            'social_science'

        ]
        


        widgets = {
    'tamil': forms.NumberInput(attrs={
             'class': 'form-control',
            # 'placeholder': 'Enter Tamil Mark',
            'required': True,
            'min': '0',
            'max': '100'
    }),
                               
    'english': forms.NumberInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter English Mark',
                'required': True,
                'min': '0',
                'max': '100'
        }),
    'maths': forms.NumberInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Maths Mark',
                'required': True,
                'min': '0',
                'max': '100'
        }),
    'science': forms.NumberInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Science Mark',
                'required': True,
                'min': '0',
                'max': '100'
        }),
    'social_science': forms.NumberInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Social Science Mark',
                'required': True,
                'min': '0',
                'max': '100'
        }),
}
        