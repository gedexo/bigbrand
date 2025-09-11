from django.urls import include, path
from . import views

app_name = "web"

urlpatterns = (
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.service, name="services"),
    path("projects/", views.project, name="projects"),  
    path("blogs/", views.blog, name="blogs"),
    path("contact/", views.contact, name="contact"),
)