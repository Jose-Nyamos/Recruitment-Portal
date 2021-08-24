from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.files.base import File
from django.db import models
from django.forms import fields
from crispy_forms.helper import FormHelper
from captcha.fields import CaptchaField
from crispy_forms.layout import Layout, Submit, Row, Column

from account.models import *


class EmployeeRegistrationForm(UserCreationForm):
    captcha = CaptchaField()


    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name :"
        self.fields['last_name'].label = "Last Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"
        self.fields['gender'].label = "Gender :"
        self.fields['captcha'].label = "captcha :"
        self.helper = FormHelper()
        self.helper.form_method = 'POST' # get or post
        self.helper.layout = Layout(
         
              Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
              Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
           
               Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
               Row(
                Column('gender', css_class='form-group col-md-6 mb-0'),
                Column('captcha', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign In')
        )

    class Meta:

        model=User

        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
                
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
    class Meta:

        model=User

        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',]


    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email =  forms.EmailField(
    widget=forms.EmailInput(attrs={ 'placeholder':'Email',})
) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={
        
        'placeholder':'Password',
    }))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

# class JobseekerBasicForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(JobseekerBasicForm, self).__init__(*args, **kwargs)
    

#     class Meta():
#         model = Jobseeker_basic
#         fields = ('profile_picture','county','subcounty','Division','Tribe','id_front','id_back','age','idnumber')
#         help_texts = {
#             'profile_picture':None,
#             'county':None,
#             'subcounty': None,
#             'Division':None,
#             'Tribe':None,
#             'id_front':None,
#             'id_back':None,
#             'idnumber':None,
#         }
#     age = forms.ChoiceField(choices=Age,widget=forms.Select)
#     idnumber = forms.CharField()
#     def clean(self):
#         all_clean_data=super().clean()
#         #age verification
#         if Age == 'Not Selected':
            # raise forms.ValidationError("Please Choose your Age")
        #phone number verificaiton
        # ph_number = all_clean_data['phone_number'].replace(" ","")
        # try:
        #  ph_number_2 = int(ph_number)
        #  if ph_number_2 < 1000000000 or ph_number_2 > 9999999999:
        #      raise forms.ValidationError(" Please Enter a valid phone number")
        # except:
        #     raise forms.ValidationError("Please enter a valid phone number")
        #phone number checking from existing users

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' # get or post
        self.helper.layout = Layout(
         
              Row(
                Column('surname', css_class='form-group col-md-3 mb-0'),
                Column('county', css_class='form-group col-md-3 mb-0'),
                Column('subcounty', css_class='form-group col-md-3 mb-0'),
                Column('Division', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
              Row(
                Column('Tribe', css_class='form-group col-md-3 mb-0'),
                Column('phone_number', css_class='form-group col-md-3 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-3 mb-0', label="Date of birth"),
                Column('idnumber', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
           
               Row(
                Column('college', css_class='form-group col-md-4 mb-0'),
                Column('course', css_class='form-group col-md-4 mb-0'),
                Column('mean_grade', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
                Row(
                Column('id_front', css_class='form-group col-md-6 mb-0'),
                Column('id_back', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                Row(
                Column('ksce_cert', css_class='form-group col-md-6 mb-0'),
                 Column('resume', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                Row(
                Column('height', css_class='form-group col-md-4 mb-0'),
                Column('weight', css_class='form-group col-md-4 mb-0'),
                Column('bmi', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
               Row(
                Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                Column('Diploma_cert', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Update')
        )
      
     

    class Meta:
        model = Profile
        fields =('surname','profile_picture','county','subcounty','Division','Tribe','phone_number','id_front','id_back','date_of_birth','idnumber'
        ,'college','course','mean_grade','ksce_cert','height','weight','bmi','resume','Diploma_cert')

    


# class JobseekerEducationForm(forms.ModelForm):

#     class Meta():
#         model = Jobseeker_education
#         fields = ('highest_education','mean_grade','ksce_cert','degree_name','diploma_name','institute','start_date','end_date')
#         help_texts = {
#             'highest_education': None,
#             'mean_grade': None,
#             'ksce_cert': None,
#             'degree_name': None,
#             'diploma_name': None,
#             'institute': None,
#             'start_date':None,
#             'end_date': None,
            
#         }
#         widgets={
#                    "start_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
#                    "end_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
#                 }
#     def clean(self):
#         all_clean_data=super().clean()
#         start_date = all_clean_data['start_date']
#         end_date = all_clean_data['end_date']
       
#         if start_date > end_date:
#             raise forms.ValidationError("end date can't be before start date")


# class JobseekerSkillForm(forms.ModelForm):

#     class Meta():
#         model = Jobseeker_skill
#         fields = ('height','weight')
#         help_texts = {
#             'height': None,
#             'weight':None,
#         }








