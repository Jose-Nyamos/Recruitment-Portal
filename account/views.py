from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from account.forms import *
from jobapp.models import*
from jobapp.permission import user_is_employee 
from django.views.generic.edit import CreateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse
import json

class AjaxExampleForm(CreateView):
    template_name = 'account/employee-registration.html'
    form_class = EmployeeRegistrationForm

    def form_invalid(self, form):
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 0
            to_json_response['form_errors'] = form.errors

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response), content_type='application/json')

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 1

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response), content_type='application/json')


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')



def employee_registration(request):

    """
    Handle Employee Registration

    """
    form = EmployeeRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/employee-registration.html',context)


def employer_registration(request):

    """
    Handle Employee Registration 

    """

    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/employer-registration.html',context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_profile(request,id):
    #User_type Table Object
    user= User.objects.get(User,id)
    #Jobseeker_basic Table Object
    jobseeker_basic_object,created = Jobseeker_basic.objects.get_or_create(user=user)
    need_update = 0 #this is for update profile notification
    if created or jobseeker_basic_object.county == 'none' :
        need_update = 1
    #for notifications
    # notification=0
    # job_post_activity_objects = Job_post_activity.objects.filter(applied_by_id=jobseeker_basic_object).order_by('-pk')
    # for object in job_post_activity_objects:
    #     if object.notification == True:
    #         notification=1
    #Jobseeker Educational details
    jobseeker_education_objects = Jobseeker_education.objects.filter(user=jobseeker_basic_object)
    #Jobseeker Work Experience Details
    jobseeker_experience_objects = Jobseeker_skill.objects.filter(user=jobseeker_basic_object)
    #Jobseeker Skillset details
   
    skill_set_objects = Jobseeker_skill.objects.all()
    return render(request,'Jobseeker/jobseeker_display_profile.html',{'jobseeker_basic':jobseeker_basic_object,'user':user,'need_update':need_update,'jobseeker_education_objects':jobseeker_education_objects,'jobseeker_experience_objects':jobseeker_experience_objects,'skill_set_objects':skill_set_objects,})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_update_profile_basic(request,id):
    #User_type Table Object
    user = User.objects.get(User)
    #Jobseeker_basic Table Object
    jobseeker_basic_object,created = Jobseeker_basic.objects.get_or_create(user=user)
    need_update = 0 #this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    #for notifications
    # notification=0
    # job_post_activity_objects = Job_post_activity.objects.filter(applied_by_id=jobseeker_basic_object).order_by('-pk')
    # for object in job_post_activity_objects:
    #     if object.notification == True:
    #         notification=1
     #Logic starts here
    if request.method=="POST":
        basic_form=JobseekerBasicForm(request.POST,request.FILES)
        if basic_form.is_valid():
            print('form is valid \n')
            jobseeker_basic_object.profile_picture = basic_form.cleaned_data['profile_picture']
            jobseeker_basic_object.county =basic_form.cleaned_data['county']
            jobseeker_basic_object.subcounty = basic_form.cleaned_data['subcounty']
            jobseeker_basic_object.Division = basic_form.cleaned_data['Division']
            jobseeker_basic_object.Tribe = basic_form.cleaned_data['Tribe']
            jobseeker_basic_object.id_front = basic_form.cleaned_data['id_front']
            jobseeker_basic_object.id_back = basic_form.cleaned_data['id_back']
            jobseeker_basic_object.idnumber = basic_form.cleaned_data['idnumber']
            jobseeker_basic_object.age = basic_form.cleaned_data['age']
            jobseeker_basic_object.save()

            # formInstance = basic_form.save(commit=False)
            # formInstance.user = user_type_user
            # formInstance.highest_education = request.POST.get('highest_education')
            # formInstance.job_type_name = request.POST.get('job_type_name')
            # formInstance.save()
            #phone number verification
            try:
                ph_object = User.objects.get(phone_number=request.POST.get('phone_number').replace(" ",""))
                if ph_object.user != request.user:
                    messages.error(request, "A user with that phone number already exists")
                    return redirect(reverse('Jobseeker:jobseeker_update_profile_basic'))
                else:
                    user.phone_number = request.POST.get('phone_number')
            except ObjectDoesNotExist:
                user.phone_number = request.POST.get('phone_number')
            user.save()
            print('\nsaved successfully')
            return redirect(reverse('account:jobseeker_profile'))

    else:
        if created==True:
            my_dict ={'phone_number':user.phone_number}
            basic_form = JobseekerBasicForm(initial=my_dict)
        else:
            my_dict = {
                           'county': jobseeker_basic_object.county,
                           'subcounty': jobseeker_basic_object.subcounty,
                           'Division': jobseeker_basic_object.Division,
                           'idnumber': jobseeker_basic_object.idnumber,
                           'phone_number': user.phone_number}

            basic_form = JobseekerBasicForm(initial=my_dict)
    return render(request,'account/jobseeker_update_profile_basic.html',{'jobseeker_basic':jobseeker_basic_object,'user':user,'need_update':0,'basic_form':basic_form,'id':id,})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_update_education(request,id):
    # User_type Table Object
    user = User.objects.get(User, id)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.county == 'none':
        need_update = 1
    #for notifications
    # notification=0
    # job_post_activity_objects = Job_post_activity.objects.filter(applied_by_id=jobseeker_basic_object).order_by('-pk')
    # for object in job_post_activity_objects:
    #     if object.notification == True:
    #         notification=1
    # Logic starts here
    if id>0:
        target_object = Jobseeker_education.objects.get(pk=id)
    if request.method == "POST":
        if id==0:
            education_form = JobseekerEducationForm(data=request.POST)
            if education_form.is_valid():
                print('form is valid \n')
                formInstance = education_form.save(commit=False)
                formInstance.user = jobseeker_basic_object
                formInstance.highest_education = request.POST.get('highest_education')
                formInstance.degree_name = request.POST.get('degree_name')
                formInstance.save()
                return redirect(reverse('account:jobseeker_profile'))
        else:
            education_form = JobseekerEducationForm(data=request.POST)
            if education_form.is_valid():
                target_object = Jobseeker_education.objects.get(pk=id)
                target_object.highest_education=request.POST.get('highest_education')
                target_object.degree_name = request.POST.get('degree_name')
                target_object.mean_grade = request.POST.get('mean_grade')
                target_object.start_date = request.POST.get('start_date')
                target_object.end_date = request.POST.get('end_date')
                target_object.institute = request.POST.get('institute')
                target_object.save()
                return redirect(reverse('account:jobseeker_profile'))

    else:
        if id==0:
            education_form = JobseekerEducationForm()
        else:
            my_dict = {'highest_education':target_object.degree_type,'degree_name':target_object.degree_name,'institute':target_object.institute,'mean_grade':target_object.mean_grade,'start_date':target_object.start_date,'end_date':target_object.end_date}
            education_form = JobseekerEducationForm(initial=my_dict)
    return render(request,'account/jobseeker_update_education.html',{'jobseeker_basic': jobseeker_basic_object, 'user': user, 'need_update': 0,'education_form': education_form,'id':id,})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_update_education_crud(request,operation,id):
    print('The operation is '+operation+"  and id is "+str(id))
    if operation=='new':
        return jobseeker_update_education(request,0)
    elif operation == 'delete':
        target_object = Jobseeker_education.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('account:jobseeker_profile'))
    elif operation=='edit':
        return jobseeker_update_education(request,id)

    #for JOBSEEKER EXPERIENCE

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_update_experience(request, id):
    # User_type Table Object
    user = User.objects.get(User, id)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.county == 'none':
        need_update = 1
    #for notifications
    # notification=0
    # job_post_activity_objects = Job_post_activity.objects.filter(applied_by_id=jobseeker_basic_object).order_by('-pk')
    # for object in job_post_activity_objects:
    #     if object.notification == True:
    #         notification=1
    # Logic starts here
    if id > 0:
        target_object = Jobseeker_skill.objects.get(pk=id)
    if request.method == "POST":
        if id == 0:
            experience_form = JobseekerSkillForm(data=request.POST)
            if experience_form.is_valid():
                print('form is valid \n')
                formInstance = experience_form.save(commit=False)
                formInstance.user = jobseeker_basic_object
                formInstance.height = request.POST.get('height')
                formInstance.weight = request.POST.get('weight')
                formInstance.save()
                return redirect(reverse('account:jobseeker_profile'))
        else:
            experience_form = JobseekerSkillForm(data=request.POST)
            if experience_form.is_valid():
                target_object = Jobseeker_skill.objects.get(pk=id)
                target_object.height = request.POST.get('height')
                target_object.weight = request.POST.get('weight')
                target_object.save()
                return redirect(reverse('account:jobseeker_profile'))

    else:
        if id == 0:
            experience_form = JobseekerSkillForm()
        else:
            my_dict = {'height':target_object.height,
            'weight': target_object.weight,  }
            experience_form = JobseekerSkillForm(initial=my_dict)
    return render(request, 'account/jobseeker_update_experience.html',
                  {'jobseeker_basic': jobseeker_basic_object, 'user': user, 'need_update': 0,
                   'experience_form': experience_form, 'id': id,})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def jobseeker_update_experience_crud(request, operation, id):
    print('The operation is ' + operation + "  and id is " + str(id))
    if operation == 'new':
        return jobseeker_update_experience(request, 0)
    elif operation == 'delete':
        target_object = Jobseeker_skill.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('account:jobseeker_profile'))
    elif operation == 'edit':
        return jobseeker_update_experience(request, id)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def employee_edit_profile(request, pk):

    """
    Handle Employee Profile Update Functionality

    """

    profile = get_object_or_404(Profile, pk=pk)
    profile, created = Profile.objects.get_or_create(user=request.user)
    need_update = 0 # this is for update of profile
    if created or profile.county == 'none' or profile.date_of_birth == 'none' or profile.mean_grade == 'none' or profile.subcounty:
        need_update = 1
    # for notification
    form = ProfileEditForm(request.POST or None ,request.FILES or None, instance=profile)
    if form.is_valid():
        form=form.save(commit=True)
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:show_profile"))
    context={
        
            'form':form,
            'need_update': need_update
        }

    return render(request,'account/employee-edit-profile.html',context)





def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    need_update = 0 # this is for update of profile
    if created or profile.county == 'none' or profile.date_of_birth == 'none' or profile.mean_grade == 'none' or profile.subcounty:
        need_update = 1

    return render(request, 'account/show_profile.html', {'need_update': need_update})

def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'account/login.html',context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')