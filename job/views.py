from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
# Create your views here.
def index(request):
    return render(request,'index.html')
def admin_login(request):
    error=""
    if request.method == 'POST':
        U = request.POST['uname']
        P = request.POST['pwd']
        user = authenticate(username=U,password=P)
        if user:
           try:
               if user.is_staff:
                   login(request,user)
                   error="no"
               else:
                   error ="yes" 
           except:
                   error = "yes"
    
    d = {'error':error}  
    return render(request,'admin_login.html',d)
def user_login(request):
    error=""
    if request.method == "POST":
       U = request.POST['uname'];
       P = request.POST['pwd'];
       user = authenticate(username=U,password=P)
       if user:
           try:
               user1 = StudentUser.objects.get(user=user)
               if user1.type == "student":
                   login(request,user)
                   error = "no"
               else:
                   error ="yes" 
           except:
               error = "yes"
       else:
           error = "yes"
    d = {'error':error}       
                             
    return render(request,'user_login.html',d)
def recruiter_login(request):
    error=""
    if request.method == "POST":
       U = request.POST['uname'];
       P = request.POST['pwd'];
       user = authenticate(username=U,password=P)
       if user:
           try:
               user1 = Recruiter.objects.get(user=user)
               if user1.type == "recruiter" and user1.status!="pending":
                   login(request,user)
                   error = "no"
               else:
                   error ="not" 
           except:
               error = "yes"
       else:
           error = "yes"
    d = {'error':error}
    return render(request,'recruiter_login.html',d)
def recruiter_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        g = request.POST['gender']
        i = request.FILES['image']
        e = request.POST['email']
        p = request.POST['pwd']
        c = request.POST['contact']
        company = request.POST['company']
        
        try:
            user = User.objects.create_user(first_name=f, last_name=l,username=e,password=p)
            Recruiter.objects.create(user=user,mobile=c,image=i,gender=g,company=company,type="recruiter",status="pending")
            error="no"
        except:
            error="yes" 
    d = {'error': error} 
    return render(request,'recruiter_signup.html',d)
def user_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        g = request.POST['gender']
        i = request.FILES['image']
        e = request.POST['email']
        p = request.POST['pwd']
        c = request.POST['contact']
        try:
            user = User.objects.create_user(first_name=f, last_name=l,username=e,password=p)
            StudentUser.objects.create(user=user,mobile=c,image=i,gender=g,type="student")
            error="no"
        except:
            error="yes" 
    d = {'error': error}     
    return render(request,'user_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        
        student.user.first_name = f
        student.user.last_name = l
        student.mobile = c
        
        
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes" 
            
        try:
            i= request.FILES['image']
            student.image = i
            student.save()
            error="no"
        except:
            pass
    
    d = {'student':student,'error':error}
    
    
    return render(request,'user_home.html',d)
def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        
        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = c
        
        
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes" 
            
        try:
            i= request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error="no"
        except:
            pass
    
    d = {'recruiter':recruiter,'error':error}
    return render(request,'recruiter_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    scount = StudentUser.objects.all().count()
    rcount = Recruiter.objects.all().count()
    jcount = Job.objects.all().count()
    d = {'scount':scount,'rcount':rcount,'jcount':jcount}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data' : data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_accepted')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status="pending") 
    d = {'data' : data}
    return render(request,'recruiter_pending.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status="Accept") 
    d = {'data' : data}
    return render(request,'recruiter_accepted.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter = Recruiter.objects.get(id=pid) 
    if request.method=="POST":
        s = request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"    
    d = {'recruiter' : recruiter,'error':error}
    return render(request,'change_status.html',d)


def change_adminpwd(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if    u.check_password(c):
                  u.set_password(n)
                  u.save()
                  error="no"
            else:
                  error="not"
        except:
                  error="yes"    
    d = {'error':error}
    return render(request,'change_adminpwd.html',d)

def change_userpwd(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if    u.check_password(c):
                  u.set_password(n)
                  u.save()
                  error="no"
            else:
                  error="not"
        except:
                  error="yes"    
    d = {'error':error}
    return render(request,'change_userpwd.html',d)

def change_recruiterpwd(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if    u.check_password(c):
                  u.set_password(n)
                  u.save()
                  error="no"
            else:
                  error="not"
        except:
                  error="yes"    
    d = {'error':error}
    return render(request,'change_recruiterpwd.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method=='POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        logo = request.FILES.get('logo')
        e = request.POST.get('experience')
        loc = request.POST.get('location')
        skills = request.POST.get('skills')
        des = request.POST.get('description')
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,tittle=jt,salary=s,image=logo,description=des,experience=e,location=loc,skills=skills,creationdate=date.today())
            error="no"
        except:
            error="yes" 
    d = {'error': error}  
    return render(request,'add_job.html',d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d = {'job':job}
    return render(request,'job_list.html',d)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id = pid)
    if request.method=='POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        e = request.POST.get('experience')
        loc = request.POST.get('location')
        skills = request.POST.get('skills')
        des = request.POST.get('description')
        
        job.tittle=jt
        job.salary=s
        job.experience=e
        job.location=loc
        job.skills=skills
        job.description=des
        
        try:
            job.save()
            error="no"
        except:
            error="yes" 
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        else:
            pass     
        
        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass 
                     
    d = {'error': error,'job': job}  
    return render(request,'edit_jobdetail.html',d)



def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id = pid)
    if request.method=='POST':
       cl = request.FILES.get('logo')
        
       job.image=cl
        
       try:
            job.save()
            error="no"
       except:
            error="yes" 
        
                     
    d = {'error': error,'job': job}  
    return render(request,'change_companylogo.html',d)

def latest_jobs(request):
    job = Job.objects.all().order_by('start_date')
    d = {'job':job}
    return render(request, 'latest_jobs.html',d)


def user_latestjobs(request):
    job = Job.objects.all().order_by('start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)
    d = {'job':job,'li':li}
    return render(request, 'user_latestjobs.html',d)


def job_detail(request,pid):
    job = Job.objects.get(id = pid)
    d = {'job':job}
    return render(request, 'job_detail.html',d)


def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect(user_login)
    
    error=""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id = pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error="notopen"
    else:
        if request.method == 'POST':
         r = request.FILES['resume']
         Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())   
         error="done"
                        
    d = {'error':error}
    return render(request, 'applyforjob.html',d)


def applied_candidate(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
 
    data = Apply.objects.all()
                     
    d = {'data': data}  
    return render(request,'applied_candidate.html',d)

def contact(request):
    return render(request,'contact.html')


def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    rcount = Recruiter.objects.all().count()
    jcount = Job.objects.all().count()
    ajcount = Apply.objects.all().count()
    d = {'rcount':rcount,'jcount':jcount,'ajcount':ajcount}
    return render(request,'user_dashboard.html',d)



def recruiter_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    scount = StudentUser.objects.all().count()
    jcount = Job.objects.all().count()
    d = {'scount':scount,'jcount':jcount}
    return render(request,'recruiter_dashboard.html',d)