from django.urls import include, path
from . import views

app_name = "web"

urlpatterns = (
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.service, name="services"),
    path("service/<slug:slug>/", views.service_detail, name="service_detail"),
    path("projects/", views.project, name="projects"),  
    path("project/<slug:slug>/", views.project_detail, name="project_detail"),
    path("blogs/", views.blog, name="blogs"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("career/", views.career, name="career"),
    path("career/<slug:slug>/", views.career_detail, name="career_detail"), 
    path("contact/", views.contact, name="contact"),
)