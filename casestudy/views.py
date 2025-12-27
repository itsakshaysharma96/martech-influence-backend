from rest_framework import viewsets, status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import CaseStudy, CaseStudyLead, CaseStudyDynamicField
from .serializers import (
    CaseStudyListSerializer, CaseStudyDetailSerializer,
    CaseStudyLeadCreateSerializer,CaseStudyDynamicFieldSerializer
)


class CaseStudyViewSet(viewsets.ViewSet):
    """
    ViewSet for Case Study - GET operations only
    """
    
    def get_queryset(self):
        queryset = CaseStudy.objects.select_related('author', 'category').filter(status='published')
        
        # Skip filtering during schema generation
        if getattr(self, 'swagger_fake_view', False) or not hasattr(self, 'request') or self.request is None:
            return queryset
        
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
        
    def dynamic_fields(self, request):
        """
        Get dynamic fields for a case study
        ?case_study_id=<id>
        """

        case_study_id = request.query_params.get('case_study_id')

        if not case_study_id:
            return create_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="case_study_id query parameter is required",
                message_code="CASE_STUDY_ID_REQUIRED",
                status=False
            )

        if not CaseStudy.objects.filter(id=case_study_id).exists():
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Case study not found",
                message_code="CASE_STUDY_NOT_FOUND",
                status=False
            )

        fields_qs = CaseStudyDynamicField.objects.filter(
            case_study_id=case_study_id,
            is_active=True
        ).order_by('sequence')

        serializer = CaseStudyDynamicFieldSerializer(fields_qs, many=True)

        return create_response(
            status_code=status.HTTP_200_OK,
            message="Case study dynamic fields retrieved successfully",
            message_code="CASE_STUDY_DYNAMIC_FIELDS_RETRIEVED",
            data={
                "case_study_id": int(case_study_id),
                "total_fields": fields_qs.count(),
                "fields": serializer.data
            }
        )
class CaseStudyLeadViewSet(viewsets.ViewSet):
    """
    ViewSet for Case Study Leads - CREATE operation only
    """

    @swagger_auto_schema(
        operation_description="""
        Submit a new case study lead/inquiry.

        **Content Type:** `application/json`

        **Field Requirements:**
        - All fields are optional
        - Recommended: `name` and `email`

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
            properties={
                'case_study': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the related case study',
                    example=1
                ),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Dynamic lead data like name, email, phone, etc.',
                    example={
                        "name": "Jane Smith",
                        "email": "jane.smith@example.com",
                        "phone": "+1234567890",
                        "company": "Tech Corp",
                        "job_title": "Marketing Manager",
                        "lead_source": "download",
                        "message": "I would like to download this case study.",
                        "utm_source": "google",
                        "utm_medium": "cpc",
                        "utm_campaign": "case_study_promo",
                        "utm_refcode": "REF456"
                    }
                )
            },
            required=[]
        ),
        responses={
            201: openapi.Response(
                description='Case study lead created successfully',
                examples={
                    "application/json": {
                        "status": True,
                        "status_code": 201,
                        "message": "Lead created successfully",
                        "message_code": "CASE_STUDY_LEAD_CREATED",
                        "data": {
                            "id": 12,
                            "case_study_id": 1,
                            "data": {
                                "name": "Jane Smith",
                                "email": "jane.smith@example.com"
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Case Study Leads']
    )
    def create(self, request):
        serializer = CaseStudyLeadCreateSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Lead created successfully",
                message_code="CASE_STUDY_LEAD_CREATED",
                data={
                    "id": lead.id,
                    "case_study_id": lead.case_study.id if lead.case_study else None,
                    "data": lead.data
                }
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid data",
            message_code="INVALID_LEAD_DATA",
            data=serializer.errors,
            status=False
        )
