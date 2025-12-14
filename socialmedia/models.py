from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class SocialMedia(TimeStampedModel):
    """Model for social media links - dynamic platform support"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('tiktok', 'TikTok'),
        ('snapchat', 'Snapchat'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('discord', 'Discord'),
        ('github', 'GitHub'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
        ('medium', 'Medium'),
        ('reddit', 'Reddit'),
        ('other', 'Other'),
    ]

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        null=True,
        blank=True,
        help_text="Social media platform"
    )
    url = models.URLField(null=True, blank=True, help_text="Social media profile URL")
    icon = models.FileField(
        upload_to='social_media_icons/',
        blank=True,
        null=True,
        help_text="Icon file for the social media platform"
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        help_text="Show this social media link on website"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description or notes"
    )

    class Meta:
        verbose_name_plural = "Social Media"
        ordering = ['platform']
        indexes = [
            models.Index(fields=['platform']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        platform_display = self.get_platform_display() if self.platform else "Unknown"
        return f"{platform_display} - {self.url or 'No URL'}"

    @property
    def display_name(self):
        """Get display name for the platform"""
        return self.get_platform_display() if self.platform else "Unknown"
