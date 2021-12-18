from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm,UserChangeForm, PasswordChangeForm
)
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .forms import NewUserForm, EditProfileForm, AddEmployeeForm, EditEmployeeForm
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import Employees,Salaries,Titles,Departments,DeptEmp,DeptManager
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q

def employee(request):
    if 'q' in request.GET:
        q=request.GET['q']
        employee=Employees.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(emp_no=q)) 
    else:
        employee = Employees.objects.all()
    p = Paginator(employee,20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context={
        'employee':page
    }
    return render(request = request,
                  template_name='main/employee.html',
                  context = context)

def add_employee(request):
   
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
            
        else:
            form = AddEmployeeForm(request.POST)
            return render(request,"main/add_employee.html",context={"form":form}) 
    form = AddEmployeeForm
    return render(request,"main/add_employee.html",context={"form":form})                    


def delete_employee(request, id):
    emp = Employees.objects.get(emp_no = id).delete()
    return redirect("/")

def detail_employee(request, id):
    emp = Employees.objects.get(emp_no = id)
    salary = Salaries.objects.filter(emp_no=id)
    title = Titles.objects.filter(emp_no=id)
    dep = Departments.objects.all()
    as_emp = DeptEmp.objects.filter(emp_no=id)
    as_man = DeptManager.objects.filter(emp_no=id)
    context={
        "employee": emp,
        "salaries":salary,
        "titles": title,
        "departments":dep,
        "as_emp": as_emp,
        "as_man": as_man,
    }
    return render(request,"main/detail_employee.html", context=context)

def edit_employee(request,id):
    emp = Employees.objects.get(emp_no = id)
    if request.method == "POST":
        form = EditEmployeeForm(request.POST, instance=emp)

        if form.is_valid():
            form.save()
            return redirect("main/edit_employee.html")
    else:
        form = EditEmployeeForm(instance=emp)
        args = {"form": form}
        return render(request,"main/edit_employee.html",args)

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    # messages.info(request, "Berhasil Keluar Akun!")
    return redirect("main:login")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request,f"Anda masuk sebagai: {username}")
                return redirect("main:home")
            else:
                messages.error(request, "Username atau Kata Sandi Tidak Sesuai")
        else:
            messages.error(request, "Username atau Kata Sandi Tidak Sesuai")
    form = AuthenticationForm()
    return render(request, 
                    "main/login.html", 
                    {"form":form})

def profile(request):
    args = {"user": request.user}
    return render(request, "main/profile.html", args)

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("main:profile")
    else:
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request,"main/edit_profile.html",args)


def about(request):
    return render(request = request,
                  template_name='main/about.html',
                  context = {})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("main:profile")
        else:
            return redirect("main:change_password")
    else:
        form = PasswordChangeForm(user=request.user)
        args = {"form": form}
        return render(request,"main/change_password.html",args)



