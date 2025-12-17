from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from tinymce.widgets import TinyMCE
from .models import ServiceCategory, Service, ServiceLead


class ServiceAdminForm(forms.ModelForm):
    """Custom form for Service admin"""
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 120, 'rows': 80}),
            'features': TinyMCE(attrs={'cols': 120, 'rows': 40}),
            'benefits': TinyMCE(attrs={'cols': 120, 'rows': 40}),
            'short_description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 100,
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;',
            }),
            'short_title': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;',
                'placeholder': 'Enter short title...'
            }),
        }


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_preview', 'is_active_badge', 'service_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'icon_preview']
    list_per_page = 25
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'icon', 'icon_preview', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 8px;" />'
                '</div>',
                obj.icon.url
            )
        return mark_safe('<span style="color: #999;">No icon</span>')
    icon_preview.short_description = 'Icon'

    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return mark_safe('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def service_count(self, obj):
        count = obj.services.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    service_count.short_description = 'Services'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = [
        'title_preview', 'short_title_preview', 'category', 'status_badge',
        'is_featured', 'is_popular', 'is_featured_badge', 'price_display',
        'inquiries_count', 'views_count', 'created_at', 'published_at'
    ]
    list_filter = [
        'status', 'is_featured', 'is_pinned', 'is_popular', 'category',
        'is_free', 'has_custom_pricing', 'created_at', 'published_at'
    ]
    search_fields = [
        'title', 'short_title', 'description', 'short_description',
        'features', 'benefits', 'meta_keywords'
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'views_count', 'inquiries_count',
        'likes_count', 'banner_image_preview', 'mobile_image_preview',
        'icon_preview', 'published_at'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_editable = ['is_featured', 'is_popular']
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'short_title', 'slug', 'category', 'author', 'status'),
            'classes': ('wide',),
        }),
        ('📄 Content', {
            'fields': ('short_description', 'description', 'features', 'benefits'),
            'classes': ('wide',),
        }),
        ('🖼️ Visual Content', {
            'fields': ('banner_image', 'banner_image_preview', 'mobile_image', 'mobile_image_preview', 'icon', 'icon_preview'),
            'classes': ('wide',),
        }),
        ('💰 Pricing Information', {
            'fields': ('price_starting_from', 'price_currency', 'price_period', 'is_free', 'has_custom_pricing'),
        }),
        ('⏱️ Service Details', {
            'fields': ('duration', 'delivery_time', 'service_type'),
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('⚙️ Settings', {
            'fields': ('is_featured', 'is_pinned', 'is_popular', 'published_at')
        }),
        ('📊 Engagement Metrics', {
            'fields': ('views_count', 'inquiries_count', 'likes_count'),
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

    def short_title_preview(self, obj):
        if obj.short_title:
            short_title = obj.short_title[:60] + "..." if len(obj.short_title) > 60 else obj.short_title
            return format_html(
                '<span style="color: #666; font-size: 12px; padding: 4px 8px; background: #f8f9fa; border-radius: 4px; display: inline-block;">{}</span>', 
                short_title
            )
        return mark_safe('<span style="color: #999;">—</span>')
    short_title_preview.short_description = 'Short Title'

    def status_badge(self, obj):
        status_colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def is_featured_badge(self, obj):
        if obj.is_featured:
            return mark_safe('<span style="background-color: #ffc107; color: #000; padding: 3px 8px; border-radius: 10px; font-size: 10px;">⭐ Featured</span>')
        return mark_safe('<span style="color: #999;">—</span>')
    is_featured_badge.short_description = 'Featured'

    def price_display(self, obj):
        if obj.is_free:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">🆓 Free</span>')
        elif obj.has_custom_pricing:
            return mark_safe('<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">💰 Custom</span>')
        elif obj.price_starting_from:
            period_text = f"/{obj.price_period}" if obj.price_period else ""
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{}{} {}</span>',
                obj.price_currency or '', obj.price_starting_from, period_text
            )
        return mark_safe('<span style="color: #999;">—</span>')
    price_display.short_description = 'Price'

    def banner_image_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<div style="margin: 15px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                '<h4 style="margin: 0 0 15px 0; color: white; font-size: 16px; font-weight: bold;">🖼️ Banner Image</h4>'
                '<img src="{}" width="100%" max-width="600" height="300" style="object-fit: cover; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 3px solid white;" />'
                '</div>',
                obj.banner_image.url
            )
        return mark_safe('<p style="color: #999; padding: 20px; background: #f5f5f5; border-radius: 4px;">No banner image uploaded</p>')
    banner_image_preview.short_description = "Banner Image Preview"

    def mobile_image_preview(self, obj):
        if obj.mobile_image:
            return format_html(
                '<div style="margin: 15px 0; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                '<h4 style="margin: 0 0 15px 0; color: white; font-size: 16px; font-weight: bold;">📱 Mobile Image</h4>'
                '<img src="{}" width="100%" max-width="400" height="250" style="object-fit: cover; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 3px solid white;" />'
                '</div>',
                obj.mobile_image.url
            )
        return mark_safe('<p style="color: #999; padding: 20px; background: #f5f5f5; border-radius: 4px;">No mobile image uploaded</p>')
    mobile_image_preview.short_description = "Mobile Image Preview"

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" width="80" height="80" style="object-fit: contain; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
                '</div>',
                obj.icon.url
            )
        return mark_safe('<span style="color: #999;">No icon uploaded</span>')
    icon_preview.short_description = "Icon Preview"

    actions = ['make_published', 'make_draft', 'make_archived']

    def make_published(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} service(s) marked as published.')
    make_published.short_description = "Mark selected services as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} service(s) marked as draft.')
    make_draft.short_description = "Mark selected services as draft"

    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} service(s) marked as archived.')
    make_archived.short_description = "Mark selected services as archived"


@admin.register(ServiceLead)
class ServiceLeadAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'service_link', 'inquiry_type_badge', 'lead_source_badge',
        'contact_status', 'conversion_status', 'utm_source', 'created_at'
    ]
    list_filter = [
        'inquiry_type', 'lead_source', 'is_contacted', 'is_converted',
        'utm_source', 'utm_campaign', 'created_at'
    ]
    search_fields = [
        'full_name', 'email', 'phone', 'company', 'service__title',
        'message', 'utm_source', 'utm_campaign'
    ]
    readonly_fields = ['created_at', 'updated_at', 'utm_summary']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('👤 Lead Information', {
            'fields': ('service', 'inquiry_type', 'lead_source', 'full_name', 'email', 'phone', 'company', 'job_title', 'message'),
            'classes': ('wide',),
        }),
        ('💼 Project Details', {
            'fields': ('budget_range', 'timeline'),
        }),
        ('📊 UTM Tracking', {
            'fields': ('utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_summary'),
            'classes': ('collapse',)
        }),
        ('✅ Status & Notes', {
            'fields': ('is_contacted', 'is_converted', 'notes')
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def service_link(self, obj):
        if obj.service:
            url = reverse('admin:services_service_change', args=[obj.service.pk])
            return format_html('<a href="{}" style="color: #007bff; text-decoration: none;">{}</a>', url, obj.service.title[:50])
        return mark_safe('<span style="color: #999;">—</span>')
    service_link.short_description = 'Service'

    def inquiry_type_badge(self, obj):
        colors = {
            'quote': '#007bff',
            'consultation': '#28a745',
            'demo': '#ffc107',
            'information': '#17a2b8',
            'custom': '#6f42c1'
        }
        color = colors.get(obj.inquiry_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_inquiry_type_display()
        )
    inquiry_type_badge.short_description = 'Inquiry Type'

    def lead_source_badge(self, obj):
        colors = {
            'website': '#007bff',
            'service_page': '#28a745',
            'phone': '#17a2b8',
            'email': '#6f42c1',
            'referral': '#ffc107',
            'social_media': '#e4405f',
            'other': '#6c757d'
        }
        color = colors.get(obj.lead_source, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">{}</span>',
            color, obj.get_lead_source_display()
        )
    lead_source_badge.short_description = 'Source'

    def contact_status(self, obj):
        if obj.is_contacted:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px;">✓ Contacted</span>')
        return mark_safe('<span style="background-color: #ffc107; color: #000; padding: 4px 10px; border-radius: 12px; font-size: 11px;">⏳ Pending</span>')
    contact_status.short_description = 'Contact'

    def conversion_status(self, obj):
        if obj.is_converted:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">💰 Converted</span>')
        return mark_safe('<span style="color: #999;">—</span>')
    conversion_status.short_description = 'Converted'

    def utm_summary(self, obj):
        utm_fields = []
        if obj.utm_source:
            utm_fields.append(f"Source: <strong>{obj.utm_source}</strong>")
        if obj.utm_medium:
            utm_fields.append(f"Medium: <strong>{obj.utm_medium}</strong>")
        if obj.utm_campaign:
            utm_fields.append(f"Campaign: <strong>{obj.utm_campaign}</strong>")
        if obj.utm_term:
            utm_fields.append(f"Term: <strong>{obj.utm_term}</strong>")
        if obj.utm_content:
            utm_fields.append(f"Content: <strong>{obj.utm_content}</strong>")
        
        if utm_fields:
            return format_html(
                '<div style="padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 10px 0;">'
                '<h4 style="margin: 0 0 10px 0; color: white;">UTM Tracking Summary</h4>'
                '<div style="line-height: 1.8;">{}</div>'
                '</div>',
                mark_safe('<br>'.join(utm_fields))
            )
        return mark_safe('<p style="color: #999; padding: 10px; background: #f5f5f5; border-radius: 4px;">No UTM tracking data available</p>')
    utm_summary.short_description = 'UTM Summary'

    actions = ['mark_as_contacted', 'mark_as_converted', 'mark_as_uncontacted', 'mark_as_unconverted']

    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(is_contacted=True)
        self.message_user(request, f'{updated} lead(s) marked as contacted.')
    mark_as_contacted.short_description = "✓ Mark selected leads as contacted"

    def mark_as_converted(self, request, queryset):
        updated = queryset.update(is_converted=True)
        self.message_user(request, f'{updated} lead(s) marked as converted.')
    mark_as_converted.short_description = "💰 Mark selected leads as converted"

    def mark_as_uncontacted(self, request, queryset):
        updated = queryset.update(is_contacted=False)
        self.message_user(request, f'{updated} lead(s) marked as not contacted.')
    mark_as_uncontacted.short_description = "Mark selected leads as not contacted"

    def mark_as_unconverted(self, request, queryset):
        updated = queryset.update(is_converted=False)
        self.message_user(request, f'{updated} lead(s) marked as not converted.')
    mark_as_unconverted.short_description = "Mark selected leads as not converted"
