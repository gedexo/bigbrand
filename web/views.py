from django.shortcuts import render

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
    context = {
        "is_project": True
    }
    return render(request, 'web/project.html', context)


def blog(request):
    context = {
        "is_blog": True
    }
    return render(request, 'web/blog.html', context)


def contact(request):
    context = {
        "is_contact": True
    }
    return render(request, 'web/contact.html', context)  