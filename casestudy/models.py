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


class CaseStudyCategory(TimeStampedModel):
    """Model for case study categories"""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Case Study Categories"
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Category"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CaseStudy(TimeStampedModel):
    """Main case study model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    short_title = models.CharField(max_length=300, null=True, blank=True, help_text="Short title or secondary heading for the case study")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_study_posts', null=True, blank=True)
    category = models.ForeignKey(CaseStudyCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='case_studies')
    
    # Content fields
    short_description = models.TextField(max_length=1000, null=True, blank=True, help_text="Extended description or summary of the case study")
    content = models.TextField(null=True, blank=True)
    banner_image = models.ImageField(upload_to='casestudy_images/banner/', blank=True, null=True, help_text="Banner image for desktop/wide screens")
    mobile_image = models.ImageField(upload_to='casestudy_images/mobile/', blank=True, null=True, help_text="Mobile optimized image for small screens")
    estimated_time = models.PositiveIntegerField(help_text="Estimated reading time in minutes", null=True, blank=True)
    
    # Case Study specific fields
    client_name = models.CharField(max_length=200, null=True, blank=True, help_text="Client or company name")
    client_industry = models.CharField(max_length=100, null=True, blank=True, help_text="Industry sector")
    project_duration = models.CharField(max_length=100, null=True, blank=True, help_text="Project duration (e.g., '3 months', '6 weeks')")
    project_budget = models.CharField(max_length=100, null=True, blank=True, help_text="Project budget range")
    results_summary = models.TextField(max_length=500, null=True, blank=True, help_text="Key results and outcomes")
    
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
    downloads_count = models.PositiveIntegerField(default=0, null=True, blank=True, help_text="Number of times case study was downloaded")
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Case Studies"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title or "Untitled Case Study"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('casestudy:detail', kwargs={'slug': self.slug})


class CaseStudyLead(TimeStampedModel):
    """Model for tracking leads generated from case studies"""
    LEAD_SOURCE_CHOICES = [
        ('download', 'Case Study Download'),
        ('contact', 'Contact Form'),
        ('demo', 'Demo Request'),
        ('consultation', 'Free Consultation'),
        ('newsletter', 'Newsletter Signup'),
        ('other', 'Other'),
    ]

    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True, help_text="Job title or position")
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
        verbose_name_plural = "Case Study Leads"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_contacted']),
            models.Index(fields=['is_converted']),
        ]

    def __str__(self):
        case_study_title = self.case_study.title if self.case_study else "No Case Study"
        name = self.name or "Anonymous"
        return f"{name} - {case_study_title}"
