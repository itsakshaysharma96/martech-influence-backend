from django.urls import path
from .views import ServiceViewSet, ServiceLeadViewSet

service_list = ServiceViewSet.as_view({'get': 'list'})
service_detail = ServiceViewSet.as_view({'get': 'retrieve'})
service_lead_create = ServiceLeadViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('services/', service_list, name='service-list'),
    path('services/<int:pk>/', service_detail, name='service-detail'),
    path('service-leads/', service_lead_create, name='service-lead-create'),
]

