from django.contrib import admin

from .models import *

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'date',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)    
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProjectImageInline]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position',)

@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)    

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "position")

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "job_category", "job_type", "opening", "last_date", "location")
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("name",)