from rest_framework import serializers
from .models import Contact


class ContactListSerializer(serializers.ModelSerializer):
    """Serializer for contact list view"""
    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'email', 'phone', 'company',
            'requirements', 'utm_source', 'utm_medium', 'utm_campaign',
            'utm_term', 'utm_content', 'created_at', 'updated_at'
        ]


class ContactDetailSerializer(serializers.ModelSerializer):
    """Serializer for contact detail view"""
    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'email', 'phone', 'company',
            'requirements', 'utm_source', 'utm_medium', 'utm_campaign',
            'utm_term', 'utm_content', 'created_at', 'updated_at'
        ]


class ContactCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contacts (public API)"""
    class Meta:
        model = Contact
        fields = [
            'full_name', 'email', 'phone', 'company', 'requirements',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'
        ]
