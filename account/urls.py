from django.urls import path
from .views import SignUpView, VerifyView, AccountCreateView, AccountList

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('list/', AccountList.as_view(), name='list')
]