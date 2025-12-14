from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import Contact
from .serializers import ContactCreateSerializer


class ContactViewSet(viewsets.ViewSet):
    """
    ViewSet for Contact - CREATE operation only (public API)
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a contact form inquiry.
        
        **Content Type:** `application/json`
        
        **Headers:**
        - `Content-Type: application/json` (Required)
        
        **Field Requirements:**
        - All fields are **optional** (can be null/blank)
        - However, it's recommended to provide at least `full_name`, `email`, and `requirements`
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'full_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Full name (optional, max 200 characters)',
                    example='John Doe'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='Email address (optional)',
                    example='john.doe@example.com'
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Phone number (optional, max 20 characters)',
                    example='+1234567890'
                ),
                'company': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Company name (optional, max 200 characters)',
                    example='Acme Corp'
                ),
                'requirements': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Message or requirements (optional)',
                    example='I am interested in your services. Please contact me.'
                ),
                'utm_source': openapi.Schema(type=openapi.TYPE_STRING, description='UTM source (optional)', example='google'),
                'utm_medium': openapi.Schema(type=openapi.TYPE_STRING, description='UTM medium (optional)', example='cpc'),
                'utm_campaign': openapi.Schema(type=openapi.TYPE_STRING, description='UTM campaign (optional)', example='contact_form'),
                'utm_term': openapi.Schema(type=openapi.TYPE_STRING, description='UTM term (optional)', example='marketing'),
                'utm_content': openapi.Schema(type=openapi.TYPE_STRING, description='UTM content (optional)', example='banner_ad'),
            },
            example={
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'company': 'Acme Corp',
                'requirements': 'I am interested in your services. Please contact me.',
                'utm_source': 'google',
                'utm_medium': 'cpc',
                'utm_campaign': 'contact_form',
                'utm_term': 'marketing',
                'utm_content': 'banner_ad'
            }
        ),
        responses={
            201: openapi.Response(description='Contact form submitted successfully'),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Contact']
    )
    def create(self, request):
        """Create a new contact (public API)"""
        serializer = ContactCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Contact form submitted successfully",
                message_code="CONTACT_CREATED",
                data=serializer.data
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Contact form submission failed",
            message_code="CONTACT_CREATION_FAILED",
            status=False,
            data=serializer.errors
        )
