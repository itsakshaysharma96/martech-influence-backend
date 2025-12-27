# apps/core/serializers/privacy_policy.py

from rest_framework import serializers
from privacy_policy.models import PrivacyPolicy

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = [
            "id",
            "title",
            "content",
            "version",
            "published_at",
            "updated_at",
        ]
