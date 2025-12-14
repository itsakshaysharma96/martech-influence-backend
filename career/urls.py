from django.urls import path
from .views import JobPostingViewSet, JobApplicationViewSet

job_posting_list = JobPostingViewSet.as_view({'get': 'list'})
job_posting_detail = JobPostingViewSet.as_view({'get': 'retrieve'})
job_application_create = JobApplicationViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('job-postings/', job_posting_list, name='job-posting-list'),
    path('job-postings/<int:pk>/', job_posting_detail, name='job-posting-detail'),
    path('job-applications/', job_application_create, name='job-application-create'),
]
