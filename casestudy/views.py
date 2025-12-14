from rest_framework import viewsets, status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import CaseStudy, CaseStudyLead
from .serializers import (
    CaseStudyListSerializer, CaseStudyDetailSerializer,
    CaseStudyLeadCreateSerializer
)


class CaseStudyViewSet(viewsets.ViewSet):
    """
    ViewSet for Case Study - GET operations only
    """
    
    def get_queryset(self):
        queryset = CaseStudy.objects.select_related('author', 'category').filter(status='published')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by client industry
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(client_industry__icontains=industry)
        
        # Filter by featured
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(content__icontains=search) |
                Q(client_name__icontains=search) |
                Q(client_industry__icontains=search)
            )
        
        # Order by
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request):
        """List all published case studies with pagination"""
        from rest_framework.pagination import PageNumberPagination
        
        queryset = self.get_queryset()
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = CaseStudyListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Case studies retrieved successfully",
                message_code="CASE_STUDIES_RETRIEVED",
                data=paginated_response.data.get('results', []),
                count=paginated_response.data.get('count', 0),
                next_link=paginated_response.data.get('next'),
                previous_link=paginated_response.data.get('previous')
            )
        
        serializer = CaseStudyListSerializer(queryset, many=True)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Case studies retrieved successfully",
            message_code="CASE_STUDIES_RETRIEVED",
            data=serializer.data
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a single case study"""
        try:
            case_study = CaseStudy.objects.select_related('author', 'category').get(pk=pk, status='published')
        except CaseStudy.DoesNotExist:
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Case study not found",
                message_code="CASE_STUDY_NOT_FOUND",
                status=False
            )
        
        # Increment views count
        case_study.views_count += 1
        case_study.save(update_fields=['views_count'])
        
        serializer = CaseStudyDetailSerializer(case_study)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Case study retrieved successfully",
            message_code="CASE_STUDY_RETRIEVED",
            data=serializer.data
        )


class CaseStudyLeadViewSet(viewsets.ViewSet):
    """
    ViewSet for Case Study Leads - CREATE operation only
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a new case study lead/inquiry.
        
        **Content Type:** `application/json`
        
        **Headers:**
        - `Content-Type: application/json` (Required)
        
        **Field Requirements:**
        - All fields are **optional** (can be null/blank)
        - However, it's recommended to provide at least `name` and `email`
        
        **Lead Source Options:**
        - `download` - Case Study Download
        - `contact` - Contact Form
        - `demo` - Demo Request
        - `consultation` - Consultation Request
        - `newsletter` - Newsletter Signup
        - `other` - Other (default)
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'case_study': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Case Study ID (optional) - ID of the case study related to this lead',
                    example=1
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Full name of the lead (optional, max 100 characters)',
                    example='Jane Smith'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='Email address of the lead (optional)',
                    example='jane.smith@example.com'
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Phone number (optional, max 20 characters)',
                    example='+1234567890'
                ),
                'company': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Company name (optional, max 100 characters)',
                    example='Tech Corp'
                ),
                'job_title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Job title or position (optional, max 100 characters)',
                    example='Marketing Manager'
                ),
                'lead_source': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['download', 'contact', 'demo', 'consultation', 'newsletter', 'other'],
                    description='Source of the lead (optional, default: "other")',
                    example='download'
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Message or inquiry details (optional)',
                    example='I would like to download this case study.'
                ),
                'utm_source': openapi.Schema(type=openapi.TYPE_STRING, description='UTM source (optional)', example='google'),
                'utm_medium': openapi.Schema(type=openapi.TYPE_STRING, description='UTM medium (optional)', example='cpc'),
                'utm_campaign': openapi.Schema(type=openapi.TYPE_STRING, description='UTM campaign (optional)', example='case_study_promo'),
                'utm_refcode': openapi.Schema(type=openapi.TYPE_STRING, description='UTM reference code (optional)', example='REF456'),
            },
            example={
                'case_study': 1,
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'phone': '+1234567890',
                'company': 'Tech Corp',
                'job_title': 'Marketing Manager',
                'lead_source': 'download',
                'message': 'I would like to download this case study.',
                'utm_source': 'google',
                'utm_medium': 'cpc',
                'utm_campaign': 'case_study_promo',
                'utm_refcode': 'REF456'
            }
        ),
        responses={
            201: openapi.Response(description='Case study lead created successfully'),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Case Study Leads']
    )
    def create(self, request):
        """Create a new case study lead"""
        serializer = CaseStudyLeadCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Case study lead submitted successfully",
                message_code="CASE_STUDY_LEAD_CREATED",
                data=serializer.data
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Case study lead submission failed",
            message_code="CASE_STUDY_LEAD_CREATION_FAILED",
            status=False,
            data=serializer.errors
        )
