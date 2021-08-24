from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from.sample import *
from account.managers import CustomUserManager
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import BaseValidator
from datetime import date
from django.urls import reverse
from django.db.models.signals import post_save
import qrcode
from io import StringIO
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from django.db import models
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('account:show_profile', args=[str(self.id)])

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'events-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - \
           ((today.month, today.day) < (born.month, born.day))

@deconstructible
class MaxAgeValidator(BaseValidator):
    message = _("Age must not be more than %(limit_value)d.")
    code = 'max_age'

    def compare(self, a, b):
        return calculate_age(a) > b

GENDER_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)
Mean_grade= (
    ('A', "A"),
    ('A-',"A-"),
    ('B+', "B+"),
    ('B',"B"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=GENDER_TYPE, max_length=1)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
   

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    surname = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='pictures/',null=False, default='../static/images/default_profile_picture.png')
    county = models.CharField(choices=new_county_1, max_length=100)
    subcounty = models.CharField(choices=new_sub_details_1, max_length=100)
    Division = models.CharField(choices=new_divisions_1,max_length=20)
    Tribe = models.CharField(choices=new_tribes_1,max_length=100)
    id_front = models.FileField(upload_to='idcard/',blank=True)
    id_back = models.FileField(upload_to='idcard/',blank=True)
    date_of_birth = models.DateField(validators=[MaxAgeValidator(26)], unique=True, null=True, blank=True )
    idnumber = models.CharField(max_length=20)
    college = models.CharField(choices=new_education_1, max_length=100)
    mean_grade = models.CharField(choices= Mean_grade, max_length=20)
    ksce_cert = models.FileField(upload_to='documents/')
    Diploma_cert = models.FileField(upload_to='documents/')
    resume = models.FileField(upload_to='resume/')
    course = models.CharField(choices = new_courses_1, max_length=70)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    height = models.FloatField( default=0)
    weight = models.FloatField(default=0)
    bmi = models.FloatField(default=0)
    emp_id = models.CharField(max_length=70, default=str(random.randrange(100,999,1)))
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

    
    def __str__(self):
        return self.user.email
       

    def get_absolute_url(self):
        return reverse('jobapp:applicant-details',  args=[str(self.pk)])  
        
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.get_absolute_url())
        canvas = Image.new('RGB', [380, 380], 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        link_qr = f'qr_code-{self.get_absolute_url()}'+ '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(link_qr, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

      
    # def generate_qrcode(self, qr):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=6,
    #         border=0,
    #     )
    #     qr.add_data(self.get_absolute_url())
    #     qr.make(fit=True)

    #     img = qr.make_image(fill='black', back_color='white')

    #     buffer = StringIO.StringIO()
    #     img.save(buffer)
    #     filename = 'events-%s.png' % (self.pk)
    #     filebuffer = InMemoryUploadedFile(
    #         buffer, None, filename, 'image/png', buffer.len, None)
    #     self.qrcode.save(filename, filebuffer)




# class Jobseeker_education(models.Model):
#     user = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
#     highest_education = models.CharField(max_length=40,default="")
#     mean_grade = models.CharField(choices= Mean_grade, max_length=20)
#     ksce_cert = models.FileField(upload_to='documents/',blank=True)
#     degree_name = models.CharField(max_length=70,blank=True)
#     diploma_name = models.CharField(max_length=70,blank=True)
#     institute = models.CharField(max_length=70)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     def __str__(self):
#         return self.user.user.email

# class Jobseeker_skill(models.Model):
#     user = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
#     height = models.IntegerField()
#     weight = models.IntegerField()
#     def __str__(self):
#         return self.user.user.email





