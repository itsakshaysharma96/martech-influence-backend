from rest_framework import viewsets, status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import Service
from .serializers import (
    ServiceListSerializer, ServiceDetailSerializer, ServiceLeadCreateSerializer
)


class ServiceViewSet(viewsets.ViewSet):
    """
    ViewSet for Service - GET operations only
    """
    
    def get_queryset(self):
        queryset = Service.objects.select_related('category', 'author').filter(status='published')
        
        # Skip filtering during schema generation
        if getattr(self, 'swagger_fake_view', False) or not hasattr(self, 'request') or self.request is None:
            return queryset
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by featured
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Filter by popular
        is_popular = self.request.query_params.get('is_popular', None)
        if is_popular is not None:
            queryset = queryset.filter(is_popular=is_popular.lower() == 'true')
        
        # Filter by free
        is_free = self.request.query_params.get('is_free', None)
        if is_free is not None:
            queryset = queryset.filter(is_free=is_free.lower() == 'true')
        
        # Filter by service type
        service_type = self.request.query_params.get('service_type', None)
        if service_type:
            queryset = queryset.filter(service_type__icontains=service_type)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description__icontains=search) |
                Q(features__icontains=search) |
                Q(benefits__icontains=search)
            )
        
        # Order by
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request):
        """List all published services with pagination"""
        from rest_framework.pagination import PageNumberPagination
        
        queryset = self.get_queryset()
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = ServiceListSerializer(page, many=True, context={'request': request})
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Services retrieved successfully",
                message_code="SERVICES_RETRIEVED",
                data=paginated_response.data.get('results', []),
                count=paginated_response.data.get('count', 0),
                next_link=paginated_response.data.get('next'),
                previous_link=paginated_response.data.get('previous')
            )
        
        serializer = ServiceListSerializer(queryset, many=True, context={'request': request})
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Services retrieved successfully",
            message_code="SERVICES_RETRIEVED",
            data=serializer.data
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a single service"""
        try:
            service = Service.objects.select_related('category', 'author').get(pk=pk, status='published')
        except Service.DoesNotExist:
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Service not found",
                message_code="SERVICE_NOT_FOUND",
                status=False
            )
        
        # Increment views count
        service.views_count += 1
        service.save(update_fields=['views_count'])
        
        serializer = ServiceDetailSerializer(service, context={'request': request})
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Service retrieved successfully",
            message_code="SERVICE_RETRIEVED",
            data=serializer.data
        )


class ServiceLeadViewSet(viewsets.ViewSet):
    """
    ViewSet for Service Leads - CREATE operation only
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a new service inquiry/lead.
        
        **Content Type:** `application/json`
        
        **Headers:**
        - `Content-Type: application/json` (Required)
        
        **Field Requirements:**
        - All fields are **optional** (can be null/blank)
        - However, it's recommended to provide at least `full_name`, `email`, and `message`
        
        **Inquiry Type Options:**
        - `quote` - Request Quote
        - `consultation` - Free Consultation
        - `demo` - Request Demo
        - `information` - General Information (default)
        - `custom` - Custom Request
        
        **Lead Source Options:**
        - `website` - Website Contact Form
        - `service_page` - Service Page
        - `phone` - Phone Call
        - `email` - Direct Email
        - `referral` - Referral
        - `social_media` - Social Media
        - `other` - Other (default)
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'service': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Service ID (optional) - ID of the service related to this inquiry',
                    example=1
                ),
                'inquiry_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['quote', 'consultation', 'demo', 'information', 'custom'],
                    description='Type of inquiry (optional, default: "information")',
                    example='quote'
                ),
                'lead_source': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['website', 'service_page', 'phone', 'email', 'referral', 'social_media', 'other'],
                    description='Source of the lead (optional, default: "website")',
                    example='website'
                ),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name (optional, max 200 characters)', example='John Doe'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address (optional)', example='john.doe@example.com'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number (optional, max 20 characters)', example='+1234567890'),
                'company': openapi.Schema(type=openapi.TYPE_STRING, description='Company name (optional, max 200 characters)', example='Acme Corp'),
                'job_title': openapi.Schema(type=openapi.TYPE_STRING, description='Job title (optional, max 100 characters)', example='Marketing Manager'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Inquiry message or requirements (optional)', example='I am interested in your services.'),
                'budget_range': openapi.Schema(type=openapi.TYPE_STRING, description='Budget range if applicable (optional, max 100 characters)', example='$10,000 - $50,000'),
                'timeline': openapi.Schema(type=openapi.TYPE_STRING, description='Project timeline if applicable (optional, max 100 characters)', example='3-6 months'),
                'utm_source': openapi.Schema(type=openapi.TYPE_STRING, description='UTM source (optional)', example='google'),
                'utm_medium': openapi.Schema(type=openapi.TYPE_STRING, description='UTM medium (optional)', example='cpc'),
                'utm_campaign': openapi.Schema(type=openapi.TYPE_STRING, description='UTM campaign (optional)', example='service_promo'),
                'utm_term': openapi.Schema(type=openapi.TYPE_STRING, description='UTM term (optional)', example='marketing'),
                'utm_content': openapi.Schema(type=openapi.TYPE_STRING, description='UTM content (optional)', example='banner_ad'),
            },
            example={
                'service': 1,
                'inquiry_type': 'quote',
                'lead_source': 'website',
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'company': 'Acme Corp',
                'job_title': 'Marketing Manager',
                'message': 'I am interested in your services.',
                'budget_range': '$10,000 - $50,000',
                'timeline': '3-6 months',
                'utm_source': 'google',
                'utm_medium': 'cpc',
                'utm_campaign': 'service_promo',
                'utm_term': 'marketing',
                'utm_content': 'banner_ad'
            }
        ),
        responses={
            201: openapi.Response(description='Service inquiry submitted successfully'),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Service Leads']
    )
    def create(self, request):
        """Create a new service lead"""
        serializer = ServiceLeadCreateSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            # Increment inquiries count for the service
            if lead.service:
                lead.service.inquiries_count += 1
                lead.service.save(update_fields=['inquiries_count'])
            
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Service inquiry submitted successfully",
                message_code="SERVICE_LEAD_CREATED",
                data=serializer.data
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Service inquiry submission failed",
            message_code="SERVICE_LEAD_CREATION_FAILED",
            status=False,
            data=serializer.errors
        )
