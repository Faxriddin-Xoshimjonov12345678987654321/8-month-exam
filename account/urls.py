from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SignUpView, VerifyView, AccountCreateView, AccountList, UpdateUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('code_verify/', VerifyView.as_view(), name='verify'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('list/', AccountList.as_view(), name='list'),
    path('update_user/', UpdateUserView.as_view()),
]