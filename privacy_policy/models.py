from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    """Abstract base model with created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        
class PrivacyPolicy(TimeStampedModel):
    title = models.CharField(max_length=255,default="Privacy Policy")
    content = models.TextField(help_text="HTML or plain text privacy policy content")
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=50,help_text="Policy version e.g. v1.0, v2.1")
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} ({self.version})"