from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Contact


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = [
#         'full_name', 'email', 'phone', 'company', 'requirements_preview',
#         'utm_source', 'created_at'
#     ]
#     list_filter = ['created_at']
#     search_fields = ['full_name', 'email', 'phone', 'company', 'requirements']
#     readonly_fields = [
#         'created_at', 'updated_at', 'utm_summary'
#     ]
#     date_hierarchy = 'created_at'
#     list_per_page = 25
    
#     fieldsets = (
#         ('👤 Contact Information', {
#             'fields': ('full_name', 'email', 'phone', 'company', 'requirements'),
#             'classes': ('wide',),
#         }),
#         ('📊 UTM Tracking', {
#             'fields': ('utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_summary'),
#             'classes': ('collapse',)
#         }),
#         ('🕐 Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

#     def requirements_preview(self, obj):
#         if obj.requirements:
#             requirements = obj.requirements[:80] + "..." if len(obj.requirements) > 80 else obj.requirements
#             return format_html('<span style="color: #333;">{}</span>', requirements)
#         return mark_safe('<span style="color: #999;">—</span>')
#     requirements_preview.short_description = 'Requirements'

#     def utm_summary(self, obj):
#         utm_fields = []
#         if obj.utm_source:
#             utm_fields.append(f"Source: <strong>{obj.utm_source}</strong>")
#         if obj.utm_medium:
#             utm_fields.append(f"Medium: <strong>{obj.utm_medium}</strong>")
#         if obj.utm_campaign:
#             utm_fields.append(f"Campaign: <strong>{obj.utm_campaign}</strong>")
#         if obj.utm_term:
#             utm_fields.append(f"Term: <strong>{obj.utm_term}</strong>")
#         if obj.utm_content:
#             utm_fields.append(f"Content: <strong>{obj.utm_content}</strong>")
        
#         if utm_fields:
#             return format_html(
#                 '<div style="padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 10px 0;">'
#                 '<h4 style="margin: 0 0 10px 0; color: white;">UTM Tracking Summary</h4>'
#                 '<div style="line-height: 1.8;">{}</div>'
#                 '</div>',
#                 mark_safe('<br>'.join(utm_fields))
#             )
#         return mark_safe('<p style="color: #999; padding: 10px; background: #f5f5f5; border-radius: 4px;">No UTM tracking data available</p>')
#     utm_summary.short_description = 'UTM Summary'
