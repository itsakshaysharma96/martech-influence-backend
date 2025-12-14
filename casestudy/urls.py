from django.urls import path
from .views import CaseStudyViewSet, CaseStudyLeadViewSet

case_study_list = CaseStudyViewSet.as_view({'get': 'list'})
case_study_detail = CaseStudyViewSet.as_view({'get': 'retrieve'})
case_study_lead_create = CaseStudyLeadViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('case-studies/', case_study_list, name='case-study-list'),
    path('case-studies/<int:pk>/', case_study_detail, name='case-study-detail'),
    path('case-study-leads/', case_study_lead_create, name='case-study-lead-create'),
]
