from django.urls import path
from .views import (
    home,
    about,
    services,
    appointment,
    gallery,
    team,
    blog,
    contact,
    services_home,
    services_blog,
    services_project,
    services_contact,
    services_single,
    services_service,
    services_about,
)


app_name = "Laboratory"


urlpatterns = [
    path("", home, name="Home"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
    path("appointment/", appointment, name="appointment"),
    path("gallery/", gallery, name="gallery"),
    path("team/", team, name="team"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
    ## Servies Web Set
    path("services_home/", services_home, name="servicesHome"),
    path("services_blog/", services_blog, name="servicesBlog"),
    path("services_project/", services_project, name="servicesProject"),
    path("services_contact/", services_contact, name="servicesContact"),
    path("services_single/", services_single, name="servicesSingle"),
    path("services_service/", services_service, name="servicesService"),
    path("services_about/", services_about, name="servicesAbout"),
]
