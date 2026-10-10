from django.urls import path
from .views import SignUpView, VerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='verify')
]