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


class ServiceCategory(TimeStampedModel):
    """Model for service categories"""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to='service_category_icons/', blank=True, null=True, help_text="Category icon")
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Category"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(TimeStampedModel):
    """Main service model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Basic Information
    title = models.CharField(max_length=200, null=True, blank=True)
    short_title = models.CharField(max_length=300, null=True, blank=True, help_text="Short title or secondary heading")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_posts')
    
    # Content fields
    short_description = models.TextField(max_length=1000, null=True, blank=True, help_text="Brief service description")
    description = models.TextField(null=True, blank=True, help_text="Full service description")
    features = models.TextField(null=True, blank=True, help_text="Key features of the service")
    benefits = models.TextField(null=True, blank=True, help_text="Benefits of using this service")
    
    # Visual Content
    banner_image = models.ImageField(upload_to='service_images/banner/', blank=True, null=True, help_text="Banner image for desktop/wide screens")
    mobile_image = models.ImageField(upload_to='service_images/mobile/', blank=True, null=True, help_text="Mobile optimized image for small screens")
    icon = models.FileField(upload_to='service_icons/', blank=True, null=True, help_text="Service icon")
    
    # Pricing Information
    price_starting_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Starting price")
    price_currency = models.CharField(max_length=10, default='USD', null=True, blank=True, help_text="Currency code")
    price_period = models.CharField(max_length=20, default='one_time', null=True, blank=True, help_text="one_time, monthly, yearly, hourly")
    is_free = models.BooleanField(default=False, null=True, blank=True, help_text="Is this a free service?")
    has_custom_pricing = models.BooleanField(default=False, null=True, blank=True, help_text="Custom pricing available")
    
    # Service Details
    duration = models.CharField(max_length=100, null=True, blank=True, help_text="Service duration (e.g., '2 weeks', '1 month')")
    delivery_time = models.CharField(max_length=100, null=True, blank=True, help_text="Expected delivery time")
    service_type = models.CharField(max_length=100, null=True, blank=True, help_text="Type of service (e.g., 'Consultation', 'Implementation')")
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated keywords for SEO")
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    is_pinned = models.BooleanField(default=False, null=True, blank=True)
    is_popular = models.BooleanField(default=False, null=True, blank=True, help_text="Mark as popular service")
    
    # Engagement metrics
    views_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    inquiries_count = models.PositiveIntegerField(default=0, null=True, blank=True, help_text="Number of service inquiries")
    likes_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Services"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title or "Untitled Service"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})


class ServiceLead(TimeStampedModel):
    """Model for tracking leads generated from services"""
    LEAD_SOURCE_CHOICES = [
        ('website', 'Website Contact Form'),
        ('service_page', 'Service Page'),
        ('phone', 'Phone Call'),
        ('email', 'Direct Email'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('other', 'Other'),
    ]

    INQUIRY_TYPE_CHOICES = [
        ('quote', 'Request Quote'),
        ('consultation', 'Free Consultation'),
        ('demo', 'Request Demo'),
        ('information', 'General Information'),
        ('custom', 'Custom Request'),
    ]

    # Service Information
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='information', null=True, blank=True)
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default='website', null=True, blank=True)
    
    # Contact Information
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Inquiry Details
    message = models.TextField(null=True, blank=True, help_text="Inquiry message or requirements")
    budget_range = models.CharField(max_length=100, blank=True, null=True, help_text="Budget range if applicable")
    timeline = models.CharField(max_length=100, blank=True, null=True, help_text="Project timeline if applicable")
    
    # Status Tracking
    is_contacted = models.BooleanField(default=False, null=True, blank=True)
    is_converted = models.BooleanField(default=False, null=True, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes about the lead")
    
    # UTM Tracking
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_term = models.CharField(max_length=100, blank=True, null=True)
    utm_content = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Service Leads"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_contacted']),
            models.Index(fields=['is_converted']),
            models.Index(fields=['service']),
        ]

    def __str__(self):
        service_title = self.service.title if self.service else "No Service"
        name = self.full_name or "Anonymous"
        return f"{name} - {service_title}"
