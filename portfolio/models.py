from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    portrait = models.ImageField(upload_to='profile/', blank=True, null=True, help_text="Photo for About Me section")
    introduction = models.TextField()
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Profile"

class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='skills/', blank=True, null=True)
    
    def __str__(self):
        return self.name

from django.utils.text import slugify

class Artwork(models.Model):
    CATEGORY_CHOICES = [
        ('PAINTING', 'Painting'),
        ('DRAWING', 'Drawing'),
        ('DIGITAL', 'Digital'),
        ('PHOTOGRAPHY', 'Photography'),
        ('MIXED_MEDIA', 'Mixed Media'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    image = models.ImageField(upload_to='artwork/')
    medium = models.CharField(max_length=100, blank=True, help_text="e.g. Oil on Canvas")
    dimensions = models.CharField(max_length=50, blank=True, help_text='e.g. 36" x 48"')
    year = models.IntegerField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True, help_text="Date the artwork was completed")
    description = models.TextField(help_text="Short description for the gallery overlay")
    content = models.TextField(blank=True, help_text="Full details/story for the detail view")
    video_url = models.URLField(blank=True, help_text="URL to video (YouTube/Vimeo) or animation")
    order = models.PositiveIntegerField(default=0, help_text="Order in the gallery (lower numbers first)")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-year', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
