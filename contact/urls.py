from django.urls import path
from .views import ContactViewSet

contact_create = ContactViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('contacts/', contact_create, name='contact-create'),
]
