from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, VerifyView, AccountCreateView, AccountList, UpdateUserView, IncomeCreateView, IncomeListView, IncomeUpdateView, IncomePartialUpdateView, IncomeDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('code_verify/', VerifyView.as_view(), name='verify'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('refresh/', TokenRefreshView.as_view(), name='login'),
    path('list/', AccountList.as_view(), name='list'),
    path('update_user/', UpdateUserView.as_view(), name='update_user'),

    path('incomes_create/', IncomeCreateView.as_view(), name='income-create'),
    path('incomes_list/', IncomeListView.as_view(), name='income-list'),
    path('incomes_update/<int:pk>/update/', IncomeUpdateView.as_view(), name='income-update'),
    path('incomes_partial_update/<int:pk>/partial-update/', IncomePartialUpdateView.as_view(), name='income-partial-update'),
    path('incomes_delete/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income-delete'),
]