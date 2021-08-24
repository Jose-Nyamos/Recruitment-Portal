from django.urls import path
from account import views

app_name = "account"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:pk>/', views.employee_edit_profile, name='edit-profile'),
    path('show_profile/', views.profile, name='show_profile'),
    # path('dashboard/employee/new/', views.Employee_New.as_view(), name='edit-profile'),
    # path('profile/<int:pk>/view/', views.Employee_View.as_view(), name='show_profile'),
    # path('profile/<int:pk>/update/', views.Employee_Update.as_view(), name='employee_update'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
]
