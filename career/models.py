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


class Department(TimeStampedModel):
    """Model for job departments"""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Department"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class JobCategory(TimeStampedModel):
    """Model for job categories"""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Category"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class JobLocation(TimeStampedModel):
    """Model for job locations"""
    name = models.CharField(max_length=100, null=True, blank=True, help_text="Location name (e.g., 'New York', 'Remote', 'London')")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_remote = models.BooleanField(default=False, null=True, blank=True, help_text="Is this a remote location?")
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Location"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class JobType(TimeStampedModel):
    """Model for job types (Full-time, Part-time, Contract, etc.)"""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="e.g., Full-time, Part-time, Contract")
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name or "Unnamed Job Type"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class JobPosting(TimeStampedModel):
    """Main job posting model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ]

    # Basic Information
    title = models.CharField(max_length=200, null=True, blank=True)
    short_title = models.CharField(max_length=300, null=True, blank=True, help_text="Short title or secondary heading")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_postings')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_postings')
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_postings')
    location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_postings')
    recruiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recruiter_jobs', help_text="Recruiter/HR responsible for this job")
    
    # Job Details
    short_description = models.TextField(max_length=1000, null=True, blank=True, help_text="Brief job description")
    job_description = models.TextField(null=True, blank=True, help_text="Full job description")
    responsibilities = models.TextField(null=True, blank=True, help_text="Key responsibilities")
    requirements = models.TextField(null=True, blank=True, help_text="Required qualifications and skills")
    preferred_qualifications = models.TextField(null=True, blank=True, help_text="Preferred but not required qualifications")
    skills_required = models.TextField(null=True, blank=True, help_text="Comma-separated list of required skills")
    
    # Compensation & Benefits
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Minimum salary")
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum salary")
    salary_currency = models.CharField(max_length=10, default='USD', null=True, blank=True, help_text="Currency code (USD, EUR, etc.)")
    salary_period = models.CharField(max_length=20, default='yearly', null=True, blank=True, help_text="yearly, monthly, hourly")
    benefits = models.TextField(null=True, blank=True, help_text="Benefits and perks")
    
    # Experience & Education
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True)
    experience_years_min = models.PositiveIntegerField(null=True, blank=True, help_text="Minimum years of experience required")
    experience_years_max = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum years of experience")
    education_required = models.CharField(max_length=200, null=True, blank=True, help_text="Required education level")
    
    # Application Details
    application_deadline = models.DateTimeField(null=True, blank=True, help_text="Application deadline")
    application_url = models.URLField(blank=True, null=True, help_text="External application URL if applicable")
    application_email = models.EmailField(blank=True, null=True, help_text="Email for applications")
    application_instructions = models.TextField(null=True, blank=True, help_text="Special application instructions")
    
    # Status & Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    is_pinned = models.BooleanField(default=False, null=True, blank=True)
    is_urgent = models.BooleanField(default=False, null=True, blank=True, help_text="Urgent/High priority position")
    
    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated keywords for SEO")
    
    # Engagement Metrics
    views_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    applications_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    shares_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True, help_text="When the job posting was closed")

    class Meta:
        verbose_name_plural = "Job Postings"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['department']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title or "Untitled Job Posting"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        # Auto-set closed_at when status changes to closed
        if self.status == 'closed' and not self.closed_at:
            from django.utils import timezone
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('career:detail', kwargs={'slug': self.slug})


class JobApplication(TimeStampedModel):
    """Model for job applications"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('offer_extended', 'Offer Extended'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_declined', 'Offer Declined'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Company Website'),
        ('job_board', 'Job Board'),
        ('referral', 'Employee Referral'),
        ('linkedin', 'LinkedIn'),
        ('indeed', 'Indeed'),
        ('glassdoor', 'Glassdoor'),
        ('other', 'Other'),
    ]

    # Application Information
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending', null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website', null=True, blank=True)
    
    # Applicant Information
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Professional Information
    current_company = models.CharField(max_length=200, blank=True, null=True)
    current_position = models.CharField(max_length=200, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notice_period = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '2 weeks', '1 month', 'Immediate'")
    
    # Documents
    resume = models.FileField(upload_to='career/resumes/', blank=True, null=True)
    cover_letter = models.FileField(upload_to='career/cover_letters/', blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    
    # Application Details
    cover_letter_text = models.TextField(blank=True, null=True, help_text="Cover letter content")
    why_interested = models.TextField(blank=True, null=True, help_text="Why are you interested in this position?")
    availability_date = models.DateField(null=True, blank=True, help_text="When can you start?")
    
    # Review Information
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes about the applicant")
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating out of 10")
    
    # Interview Information
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=200, blank=True, null=True)
    interview_notes = models.TextField(blank=True, null=True)
    
    # Offer Information
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_date = models.DateTimeField(null=True, blank=True)
    offer_deadline = models.DateTimeField(null=True, blank=True)
    
    # UTM Tracking
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_refcode = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Job Applications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['job_posting']),
        ]

    def __str__(self):
        job_title = self.job_posting.title if self.job_posting else "No Job"
        name = f"{self.first_name} {self.last_name}".strip() if self.first_name or self.last_name else "Anonymous"
        return f"{name} - {job_title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
