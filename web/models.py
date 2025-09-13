from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse_lazy


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("web:blog_detail", kwargs={"slug": self.slug})
    

    class Meta:
        ordering = ['-date']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'


class Project(models.Model):
    category = models.ForeignKey("web.ProjectCategory", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='project_images')
    client = models.CharField(max_length=100, null=True)
    timescale = models.CharField(max_length=100, null=True)
    launch_date = models.DateField(null=True)
    project_url = models.URLField(blank=True, null=True)
    description = HTMLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("web:project_detail", kwargs={"slug": self.slug})

    def get_images(self):
        return ProjectImage.objects.filter(project=self).order_by('order_id')

    def get_image_classes(self):
        pattern = ["col-lg-12", "col-lg-6", "col-lg-6", "col-lg-4", "col-lg-4", "col-lg-4"]
        return [(img, pattern[i % len(pattern)]) for i, img in enumerate(self.get_images())]

    class Meta:
        ordering = ['-id']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    
class ProjectImage(models.Model):
    order_id = models.PositiveIntegerField()
    project = models.ForeignKey("web.Project", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images')

    def __str__(self):
        return self.project.name

    class Meta:
        ordering = ['order_id']
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='service_images')
    description = HTMLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("web:service_detail", kwargs={"slug": self.slug})
    

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonial_images')
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    
class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='client_images')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Client Logo'
        verbose_name_plural = 'Client Logos'

    
class HeroBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hero_images')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    
class Team(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    
class Career(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    job_category = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    opening = models.PositiveIntegerField()
    last_date = models.DateField()
    location = models.CharField(max_length=100) 
    description = HTMLField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("web:career_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'

    
class CareerEnquiry(models.Model):
    career = models.ForeignKey("web.Career", verbose_name="Position", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Career Enquiry'
        verbose_name_plural = 'Career Enquiries'

    
class Gallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery_images')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'