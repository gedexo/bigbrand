from django.urls import include, path
from . import views

app_name = "web"

urlpatterns = (
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.service, name="services"),
    path("projects/", views.project, name="projects"),  
    path("project/<slug:slug>/", views.project_detail, name="project_detail"),
    path("blogs/", views.blog, name="blogs"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
)