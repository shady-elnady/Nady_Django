from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Doctor.models import Doctor

# Create your views here.



app_name = "Laboratory"

@login_required
def home(req):
    return render(req, f"{app_name}/home.html")

# @login_required
# def about(req):
#     return render(req, f"{app_name}/about.html")
def about(req):
    return render(req, f"account/login.html")

# @login_required
def services(req):
    return render(req, f"{app_name}/services.html")

# @login_required
def appointment(req):
    return render(req, f"{app_name}/appointment.html")

# @login_required
def gallery(req):
    return render(req, f"{app_name}/gallery.html")

# @login_required
def team(req):
    doctors = Doctor.objects.all()
    context = {
        "doctors": doctors,
    }
    for doctor in doctors:
        print(doctor.name)
        print(doctor.image)
        print(doctor.job)
        print(doctor.social_media.all())

    return render(req, f"{app_name}/team.html", context= context)

# @login_required
def blog(req):
    return render(req, f"{app_name}/blog.html")

# @login_required
def contact(req):
    return render(req, f"{app_name}/contact.html")


### https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html



############################################

services_name= "Services"


context= {
    "app_name": services_name
}


def services_home(req):
    context["page_name"]= "home"
    return render(req, f"{services_name}/index.html", context= context)


def services_blog(req):
    context["page_name"]= "blog"
    return render(req, f"{services_name}/blog.html", context= context)


def services_about(req):
    context["page_name"]= "about"
    return render(req, f"{services_name}/about.html", context= context)


def services_contact(req):
    context["page_name"]= "contact"
    return render(req, f"{services_name}/contact.html", context= context)


def services_project(req):
    context["page_name"]= "project"
    return render(req, f"{services_name}/project.html", context= context)


def services_service(req):
    context["page_name"]= "service"
    return render(req, f"{services_name}/service.html", context= context)


def services_single(req):
    context["page_name"]= "single"
    return render(req, f"{services_name}/single.html", context= context)
