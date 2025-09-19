from django.db.models import Q
import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .forms import ContactForm, CareerEnquiryForm, ServiceEnquiryForm
from .models import Blog, Meta, ProjectCategory, Project, ClientLogo, Service, FAQ, Testimonial, Career, Gallery, Team


def index(request):
    service = Service.objects.all()
    projects = Project.objects.all()[:6]
    testimonials = Testimonial.objects.all()
    meta = Meta.objects.filter(page='home').first()
    context = {
        "is_home": True,
        "services": service,
        "projects": projects,
        "testimonials": testimonials,
        "meta":meta
    }
    return render(request, 'web/index.html', context)


def about(request):
    services = Service.objects.all()
    faqs = FAQ.objects.all()    
    testimonials = Testimonial.objects.all()
    teams = Team.objects.all()
    context = {
        "is_about": True,
        "services": services,
        "faqs": faqs,
        "testimonials": testimonials,
        "teams": teams,
        "meta": Meta.objects.filter(page='about').first()
    }
    return render(request, 'web/about.html', context)


def service(request):
    services = Service.objects.all()
    context = {
        "is_service": True,
        "services": services,
        "meta": Meta.objects.filter(page='service').first()
    }
    return render(request, 'web/service.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    form = ServiceEnquiryForm(request.POST or None)

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
                "message": "Your enquiry has been submitted successfully.",
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
        "is_service": True,
        "service": service,
        "form": form,
        "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_SITE_KEY,
    }
    return render(request, "web/service-detail.html", context)


def project(request):
    project_categories = ProjectCategory.objects.all()
    clients = ClientLogo.objects.all()
    
    # Get the category from GET parameters
    category_name = request.GET.get('category')
    
    if category_name:
        # Filter projects by category name
        projects = Project.objects.filter(category__name=category_name)
    else:
        # Show all projects if no category is selected
        projects = Project.objects.all()
    
    context = {
        "is_project": True,
        "project_categories": project_categories,
        "projects": projects,
        "clients": clients,
        "selected_category": category_name,
        "meta": Meta.objects.filter(page='project').first()
    }
    
    return render(request, 'web/project.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Adjust according to Meta ordering = ['-id']
    next_project = Project.objects.filter(id__lt=project.id).order_by('-id').first()
    prev_project = Project.objects.filter(id__gt=project.id).order_by('id').first()
    
    context = {
        "is_project": True,
        "project": project,
        "next_project": next_project,
        "prev_project": prev_project
    }
    return render(request, "web/project-detail.html", context)


def blog(request):
    blogs_list = Blog.objects.all().order_by("-date")
    paginator = Paginator(blogs_list, 6)

    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    context = {
        "is_blog": True,
        "blogs": blogs,
        "blog": Meta.objects.filter(page='blog').first()
    }
    return render(request, "web/blog.html", context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    query = request.GET.get('q', '')
    
    if query:
        other_blogs = Blog.objects.exclude(slug=slug).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        other_blogs = Blog.objects.exclude(slug=slug)
    
    next_blog = Blog.objects.filter(id__gt=blog.id).order_by("id").first()
    
    context = {
        "is_blog": True,
        "blog": blog,
        "other_blogs": other_blogs,
        "next_blog": next_blog,
        "search_query": query,
    }
    return render(request, "web/blog-detail.html", context)


def career(request):
    galleries = Gallery.objects.all()
    context = {
        "is_career": True,
        "careers": Career.objects.all(),
        "galleries": galleries,
        "career": Meta.objects.filter(page='career').first()
    }
    return render(request, "web/career.html", context)   


def career_detail(request, slug):
    career = get_object_or_404(Career, slug=slug)
    form = CareerEnquiryForm()

    if request.method == "POST":
        form = CareerEnquiryForm(request.POST, request.FILES)

        # Turnstile response token
        token = request.POST.get("cf-turnstile-response")

        # Verify with Cloudflare Turnstile
        verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        data = {
            "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
        resp = requests.post(verify_url, data=data)
        result = resp.json()

        if not result.get("success"):
            # Captcha failed
            response_data = {
                "success": False,
                "errors": {"__all__": ["Captcha verification failed. Please try again."]}
            }
            return JsonResponse(response_data)

        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.career = career
            enquiry.save()
            response_data = {
                "success": True,
                "message": "Your application has been received successfully!",
            }
        else:
            # Return field-specific errors
            response_data = {
                "success": False,
                "errors": form.errors,  # Django returns errors as a dict
            }

        return JsonResponse(response_data)

    context = {
        "is_career": True,
        "career": career,
        "form": form,
        "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_SITE_KEY,
    }
    return render(request, "web/career-detail.html", context)


def gallery(request):
    galleries = Gallery.objects.all()
    context = {
        "is_gallery": True,
        "galleries": galleries,
        "gallery": Meta.objects.filter(page='gallery').first()
    }
    return render(request, "web/gallery.html", context)
    

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
        "contact": Meta.objects.filter(page='contact').first()
    }
    return render(request, "web/contact.html", context)