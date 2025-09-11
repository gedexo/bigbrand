from django.db import models
from tinymce.models import HTMLField


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Blog(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog_images')
    date = models.DateField()
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='Administrator')
    description = HTMLField()

    def str(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'


class Project(models.Model):
    category = models.ForeignKey("web.ProjectCategory", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='project_images')
    description = HTMLField()

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    
class ProjectImage(models.Model):
    project = models.ForeignKey("web.Project", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images')

    def str(self):
        return self.project.name

    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='service_images')
    description = HTMLField()

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonial_images')
    content = models.TextField()

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    
class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='client_images')

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Client Logo'
        verbose_name_plural = 'Client Logos'

    
class HeroBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hero_images')

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'

    
