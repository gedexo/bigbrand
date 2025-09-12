import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .forms import ContactForm
from .models import Blog, ProjectCategory, Project, ClientLogo


def index(request):

    context = {
        "is_home": True
    }
    return render(request, 'web/index.html', context)


def about(request):
    context = {
        "is_about": True
    }
    return render(request, 'web/about.html', context)

def service(request):
    context = {
        "is_service": True
    }
    return render(request, 'web/service.html', context)


def project(request):
    project_categories = ProjectCategory.objects.all()
    projects =  Project.objects.all()
    clients = ClientLogo.objects.all()
    context = {
        "is_project": True,
        "project_categories": project_categories,
        "projects": projects,
        "clients": clients
    }
    return render(request, 'web/project.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    next_project = Project.objects.filter(id__gt=project.id).order_by("id").first()
    context = {
        "is_project": True,
        "project": project,
        "next_project": next_project
    }
    return render(request, "web/project-detail.html", context)


def blog(request):
    blogs_list = Blog.objects.all().order_by("-date")
    paginator = Paginator(blogs_list, 6)

    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    context = {
        "is_blog": True,
        "blogs": blogs
    }
    return render(request, "web/blog.html", context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    other_blogs = Blog.objects.exclude(slug=slug)
    
    next_blog = Blog.objects.filter(id__gt=blog.id).order_by("id").first()
    
    context = {
        "is_blog": True,
        "blog": blog,
        "other_blogs": other_blogs,
        "next_blog": next_blog,
    }
    return render(request, "web/blog-detail.html", context)


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        # Get Turnstile response token from frontend
        token = request.POST.get("cf-turnstile-response")

        # Verify with Cloudflare
        verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        data = {
            "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
        resp = requests.post(verify_url, data=data)
        result = resp.json()

        if result.get("success") and form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
            }
        else:
            # Debugging
            print("Form errors:", form.errors)
            print("Captcha result:", result)

            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": "Captcha failed or invalid input.",
            }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/javascript",
        )

    # GET request → render form
    context = {
        "is_contact": True,
        "form": form,
        "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_SITE_KEY,
    }
    return render(request, "web/contact.html", context)