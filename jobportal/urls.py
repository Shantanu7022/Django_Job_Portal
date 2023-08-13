"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('index', index, name="index"),
    path('admin_login', admin_login, name="admin_login"),
    path('user_login', user_login, name="user_login"),
    path('user_signup', user_signup, name="user_signup"),
    path('recruiter_signup', recruiter_signup, name="recruiter_signup"),
    path('recruiter_login', recruiter_login, name="recruiter_login"),
    path('user_home', user_home, name="user_home"),
    path('recruiter_home', recruiter_home, name="recruiter_home"),
    path('admin_home', admin_home, name="admin_home"),
    path('view_users', view_users, name="view_users"),
    path('Logout', Logout, name="Logout"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('change_status/<int:pid>', change_status, name="change_status"),
    path('recruiter_pending', recruiter_pending, name="recruiter_pending"),
    path('recruiter_accepted', recruiter_accepted, name="recruiter_accepted"),
    path('delete_recruiter/<int:pid>', delete_recruiter, name="delete_recruiter"),
    path('change_adminpwd', change_adminpwd, name="change_adminpwd"),
    path('change_userpwd', change_userpwd, name="change_userpwd"),
    path('change_recruiterpwd', change_recruiterpwd, name="change_recruiterpwd"),
    path('add_job', add_job, name="add_job"),   
    path('job_list', job_list, name="job_list"),  
    path('edit_jobdetail/<int:pid>', edit_jobdetail, name="edit_jobdetail"),
    path('change_companylogo/<int:pid>', change_companylogo, name="change_companylogo"),
    path('latest_jobs', latest_jobs, name="latest_jobs"),  
    path('user_latestjobs', user_latestjobs, name="user_latestjobs"),  
    path('job_detail/<int:pid>', job_detail, name="job_detail"),
    path('applyforjob/<int:pid>', applyforjob, name="applyforjob"),   
    path('applied_candidate', applied_candidate, name="applied_candidate"), 
    path('contact', contact, name="contact"),
    path('user_dashboard', user_dashboard, name="user_dashboard"), 
    path('recruiter_dashboard', recruiter_dashboard, name="recruiter_dashboard"),        
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

