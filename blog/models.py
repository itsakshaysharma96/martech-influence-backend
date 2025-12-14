from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base model with created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """Model for blog categories"""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Category"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(TimeStampedModel):
    """Model for blog tags"""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Tag"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(TimeStampedModel):
    """Main blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    short_title = models.CharField(max_length=300, null=True, blank=True, help_text="Short title or secondary heading for the blog post")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    tags = models.ManyToManyField(Tag, blank=True, related_name='blogs')
    
    # Content fields
    short_description = models.TextField(max_length=1000, null=True, blank=True, help_text="Extended description or summary of the blog post")
    content = models.TextField(null=True, blank=True)
    banner_image = models.ImageField(upload_to='blog_images/banner/', blank=True, null=True, help_text="Banner image for desktop/wide screens")
    mobile_image = models.ImageField(upload_to='blog_images/mobile/', blank=True, null=True, help_text="Mobile optimized image for small screens")
    estimated_time = models.PositiveIntegerField(help_text="Estimated reading time in minutes", null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated keywords for SEO")
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    is_pinned = models.BooleanField(default=False, null=True, blank=True)
    
    # Engagement metrics
    views_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    shares_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title or "Untitled Blog"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


class BlogLeads(TimeStampedModel):
    """Model for tracking leads generated from blog posts"""
    LEAD_SOURCE_CHOICES = [
        ('newsletter', 'Newsletter Signup'),
        ('download', 'Resource Download'),
        ('contact', 'Contact Form'),
        ('demo', 'Demo Request'),
        ('other', 'Other'),
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default='other', null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    is_contacted = models.BooleanField(default=False, null=True, blank=True)
    is_converted = models.BooleanField(default=False, null=True, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes about the lead")
    
    # UTM Tracking fields
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_refcode = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Blog Leads"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_contacted']),
            models.Index(fields=['is_converted']),
        ]

    def __str__(self):
        blog_title = self.blog.title if self.blog else "No Blog"
        name = self.name or "Anonymous"
        return f"{name} - {blog_title}"
