from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from tinymce.widgets import TinyMCE
from .models import (
    Department, JobCategory, JobLocation, JobType,
    JobPosting, JobApplication
)


class JobPostingAdminForm(forms.ModelForm):
    """Custom form for Job Posting admin"""
    class Meta:
        model = JobPosting
        fields = '__all__'
        widgets = {
            'job_description': TinyMCE(attrs={'cols': 120, 'rows': 80}),
            'responsibilities': TinyMCE(attrs={'cols': 120, 'rows': 40}),
            'requirements': TinyMCE(attrs={'cols': 120, 'rows': 40}),
            'preferred_qualifications': TinyMCE(attrs={'cols': 120, 'rows': 30}),
            'short_description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 100,
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;',
            }),
            'short_title': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;',
                'placeholder': 'Enter short title...'
            }),
            'benefits': forms.Textarea(attrs={
                'rows': 4,
                'cols': 100,
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;',
            }),
        }


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active_badge', 'job_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def job_count(self, obj):
        count = obj.job_postings.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    job_count.short_description = 'Jobs'


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active_badge', 'job_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def job_count(self, obj):
        count = obj.job_postings.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    job_count.short_description = 'Jobs'


@admin.register(JobLocation)
class JobLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'country', 'is_remote_badge', 'is_active_badge', 'job_count', 'created_at']
    list_filter = ['is_remote', 'is_active', 'country', 'state', 'created_at']
    search_fields = ['name', 'city', 'state', 'country']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'slug', 'city', 'state', 'country', 'is_remote', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_remote_badge(self, obj):
        if obj.is_remote:
            return format_html('<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">🌐 Remote</span>')
        return format_html('<span style="color: #999;">—</span>')
    is_remote_badge.short_description = 'Remote'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def job_count(self, obj):
        count = obj.job_postings.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    job_count.short_description = 'Jobs'


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active_badge', 'job_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Job Type Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def job_count(self, obj):
        count = obj.job_postings.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    job_count.short_description = 'Jobs'


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    form = JobPostingAdminForm
    list_display = [
        'title_preview', 'department', 'category', 'location_display', 'job_type',
        'status_badge', 'is_featured', 'is_urgent', 'experience_level_display',
        'salary_display', 'applications_count', 'views_count', 'published_at', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'is_pinned', 'is_urgent', 'department', 'category',
        'job_type', 'location', 'experience_level', 'created_at', 'published_at'
    ]
    search_fields = [
        'title', 'short_title', 'job_description', 'short_description',
        'requirements', 'skills_required', 'meta_keywords'
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'views_count', 'applications_count',
        'shares_count', 'published_at', 'closed_at'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_editable = ['is_featured', 'is_urgent']
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'short_title', 'slug', 'department', 'category', 'job_type', 'location', 'recruiter', 'status'),
            'classes': ('wide',),
        }),
        ('💼 Job Details', {
            'fields': ('short_description', 'job_description', 'responsibilities', 'requirements', 'preferred_qualifications', 'skills_required'),
            'classes': ('wide',),
        }),
        ('💰 Compensation & Benefits', {
            'fields': ('salary_min', 'salary_max', 'salary_currency', 'salary_period', 'benefits'),
        }),
        ('🎓 Experience & Education', {
            'fields': ('experience_level', 'experience_years_min', 'experience_years_max', 'education_required'),
        }),
        ('📋 Application Details', {
            'fields': ('application_deadline', 'application_url', 'application_email', 'application_instructions'),
        }),
        ('⚙️ Settings', {
            'fields': ('is_featured', 'is_pinned', 'is_urgent', 'published_at', 'closed_at'),
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('📊 Engagement Metrics', {
            'fields': ('views_count', 'applications_count', 'shares_count'),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def title_preview(self, obj):
        title = obj.title or "Untitled"
        if len(title) > 50:
            title = title[:50] + "..."
        return format_html('<strong style="color: #333;">{}</strong>', title)
    title_preview.short_description = 'Title'

    def location_display(self, obj):
        if obj.location:
            location = obj.location.name
            if obj.location.is_remote:
                return format_html('<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">🌐 {}</span>', location)
            return format_html('<span style="color: #666;">📍 {}</span>', location)
        return format_html('<span style="color: #999;">—</span>')
    location_display.short_description = 'Location'

    def status_badge(self, obj):
        status_colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'closed': '#dc3545',
            'archived': '#6c757d'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def experience_level_display(self, obj):
        if obj.experience_level:
            colors = {
                'entry': '#28a745',
                'mid': '#ffc107',
                'senior': '#fd7e14',
                'executive': '#dc3545'
            }
            color = colors.get(obj.experience_level, '#6c757d')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">{}</span>',
                color, obj.get_experience_level_display()
            )
        return format_html('<span style="color: #999;">—</span>')
    experience_level_display.short_description = 'Level'

    def salary_display(self, obj):
        if obj.salary_min and obj.salary_max:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{}{} - {}{} {}</span>',
                obj.salary_currency or '', obj.salary_min, obj.salary_currency or '', obj.salary_max,
                f'/{obj.salary_period}' if obj.salary_period else ''
            )
        elif obj.salary_min:
            return format_html('<span style="color: #28a745;">{}{}+ {}</span>', obj.salary_currency or '', obj.salary_min, f'/{obj.salary_period}' if obj.salary_period else '')
        return format_html('<span style="color: #999;">—</span>')
    salary_display.short_description = 'Salary'

    actions = ['make_published', 'make_closed', 'make_draft', 'make_archived']

    def make_published(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} job posting(s) marked as published.')
    make_published.short_description = "Mark selected jobs as published"

    def make_closed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='closed', closed_at=timezone.now())
        self.message_user(request, f'{updated} job posting(s) marked as closed.')
    make_closed.short_description = "Mark selected jobs as closed"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} job posting(s) marked as draft.')
    make_draft.short_description = "Mark selected jobs as draft"

    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} job posting(s) marked as archived.')
    make_archived.short_description = "Mark selected jobs as archived"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'applicant_name', 'job_posting_link', 'status_badge', 'source_badge',
        'experience_display', 'current_company', 'rating_display',
        'reviewed_by', 'interview_date', 'created_at'
    ]
    list_filter = [
        'status', 'source', 'job_posting', 'reviewed_by',
        'interview_date', 'created_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'phone', 'current_company',
        'current_position', 'job_posting__title'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'reviewed_at', 'applicant_info_display',
        'resume_preview', 'cover_letter_preview', 'utm_summary'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('📋 Application Information', {
            'fields': ('job_posting', 'status', 'source', 'applicant_info_display')
        }),
        ('👤 Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'country', 'zip_code')
        }),
        ('💼 Professional Information', {
            'fields': ('current_company', 'current_position', 'years_of_experience', 'current_salary', 'expected_salary', 'notice_period')
        }),
        ('📄 Documents & Links', {
            'fields': ('resume', 'resume_preview', 'cover_letter', 'cover_letter_preview', 'portfolio_url', 'linkedin_url', 'github_url')
        }),
        ('✍️ Application Details', {
            'fields': ('cover_letter_text', 'why_interested', 'availability_date')
        }),
        ('👨‍💼 Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'notes', 'rating')
        }),
        ('📅 Interview Information', {
            'fields': ('interview_date', 'interview_location', 'interview_notes')
        }),
        ('💰 Offer Information', {
            'fields': ('offer_amount', 'offer_date', 'offer_deadline')
        }),
        ('📊 UTM Tracking', {
            'fields': ('utm_source', 'utm_medium', 'utm_campaign', 'utm_refcode', 'utm_summary'),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def applicant_name(self, obj):
        name = obj.full_name or "Anonymous"
        return format_html('<strong>{}</strong>', name)
    applicant_name.short_description = 'Applicant'

    def applicant_info_display(self, obj):
        info = []
        if obj.email:
            info.append(f"📧 {obj.email}")
        if obj.phone:
            info.append(f"📞 {obj.phone}")
        if obj.current_company:
            info.append(f"🏢 {obj.current_company}")
        if obj.years_of_experience:
            info.append(f"⏱ {obj.years_of_experience} years")
        
        if info:
            return format_html(
                '<div style="padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 10px 0;">'
                '<h4 style="margin: 0 0 10px 0; color: white;">Applicant Information</h4>'
                '<div style="line-height: 1.8;">{}</div>'
                '</div>',
                mark_safe('<br>'.join(info))
            )
        return format_html('<p style="color: #999;">No additional information</p>')
    applicant_info_display.short_description = 'Applicant Info'

    def job_posting_link(self, obj):
        if obj.job_posting:
            url = reverse('admin:career_jobposting_change', args=[obj.job_posting.pk])
            return format_html('<a href="{}" style="color: #007bff; text-decoration: none;">{}</a>', url, obj.job_posting.title[:50])
        return format_html('<span style="color: #999;">—</span>')
    job_posting_link.short_description = 'Job Posting'

    def status_badge(self, obj):
        status_colors = {
            'pending': '#ffc107',
            'reviewing': '#17a2b8',
            'shortlisted': '#28a745',
            'interview_scheduled': '#007bff',
            'interviewed': '#6f42c1',
            'offer_extended': '#fd7e14',
            'offer_accepted': '#28a745',
            'offer_declined': '#dc3545',
            'rejected': '#dc3545',
            'withdrawn': '#6c757d'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def source_badge(self, obj):
        colors = {
            'website': '#007bff',
            'job_board': '#28a745',
            'referral': '#ffc107',
            'linkedin': '#0077b5',
            'indeed': '#2164f3',
            'glassdoor': '#0caa41',
            'other': '#6c757d'
        }
        color = colors.get(obj.source, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">{}</span>',
            color, obj.get_source_display()
        )
    source_badge.short_description = 'Source'

    def experience_display(self, obj):
        if obj.years_of_experience:
            return format_html('<span style="color: #666;">{} years</span>', obj.years_of_experience)
        return format_html('<span style="color: #999;">—</span>')
    experience_display.short_description = 'Experience'

    def rating_display(self, obj):
        if obj.rating:
            color = '#28a745' if obj.rating >= 7 else '#ffc107' if obj.rating >= 5 else '#dc3545'
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">⭐ {}/10</span>',
                color, obj.rating
            )
        return format_html('<span style="color: #999;">—</span>')
    rating_display.short_description = 'Rating'

    def resume_preview(self, obj):
        if obj.resume:
            return format_html(
                '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 5px 0;">'
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">📄 View Resume</a>'
                '</div>',
                obj.resume.url
            )
        return format_html('<span style="color: #999;">No resume uploaded</span>')
    resume_preview.short_description = 'Resume'

    def cover_letter_preview(self, obj):
        if obj.cover_letter:
            return format_html(
                '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 5px 0;">'
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">📝 View Cover Letter</a>'
                '</div>',
                obj.cover_letter.url
            )
        return format_html('<span style="color: #999;">No cover letter uploaded</span>')
    cover_letter_preview.short_description = 'Cover Letter'

    def utm_summary(self, obj):
        utm_fields = []
        if obj.utm_source:
            utm_fields.append(f"Source: <strong>{obj.utm_source}</strong>")
        if obj.utm_medium:
            utm_fields.append(f"Medium: <strong>{obj.utm_medium}</strong>")
        if obj.utm_campaign:
            utm_fields.append(f"Campaign: <strong>{obj.utm_campaign}</strong>")
        if obj.utm_refcode:
            utm_fields.append(f"Ref Code: <strong>{obj.utm_refcode}</strong>")
        
        if utm_fields:
            return format_html(
                '<div style="padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 10px 0;">'
                '<h4 style="margin: 0 0 10px 0; color: white;">UTM Tracking Summary</h4>'
                '<div style="line-height: 1.8;">{}</div>'
                '</div>',
                mark_safe('<br>'.join(utm_fields))
            )
        return format_html('<p style="color: #999; padding: 10px; background: #f5f5f5; border-radius: 4px;">No UTM tracking data available</p>')
    utm_summary.short_description = 'UTM Summary'

    actions = ['mark_shortlisted', 'mark_rejected', 'mark_interview_scheduled']

    def mark_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} application(s) marked as shortlisted.')
    mark_shortlisted.short_description = "Mark selected as shortlisted"

    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) marked as rejected.')
    mark_rejected.short_description = "Mark selected as rejected"

    def mark_interview_scheduled(self, request, queryset):
        updated = queryset.update(status='interview_scheduled')
        self.message_user(request, f'{updated} application(s) marked as interview scheduled.')
    mark_interview_scheduled.short_description = "Mark selected as interview scheduled"
