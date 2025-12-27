from django.urls import path
from .views import PrivacyPolicyViewSet

privacy_policy_list = PrivacyPolicyViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('list/', privacy_policy_list, name='privacy-policy-list'),
]
