from django.urls import path
from .views import CaseStudyViewSet, CaseStudyLeadViewSet

case_study_list = CaseStudyViewSet.as_view({'get': 'list'})
case_study_detail = CaseStudyViewSet.as_view({'get': 'retrieve'})
case_study_lead_create = CaseStudyLeadViewSet.as_view({'post': 'create'})
case_study_dynamic_fields = CaseStudyViewSet.as_view({'get': 'dynamic_fields'}) 

urlpatterns = [
    path('case-studies/', case_study_list, name='case-study-list'),
    path('case-studies/<int:pk>/', case_study_detail, name='case-study-detail'),
    path('case-studies/dynamic-fields/', case_study_dynamic_fields, name='case-study-dynamic-fields'),
    path('case-study-leads/', case_study_lead_create, name='case-study-lead-create'),
]
