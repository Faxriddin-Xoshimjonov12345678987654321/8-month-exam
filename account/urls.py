from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, VerifyView, AccountCreateView, AccountList, UpdateUserView, IncomeCreateView, IncomeListView, IncomeUpdateView, IncomePartialUpdateView, IncomeDeleteView, ExpenseCreateView, ExpenseListView, ExpenseUpdateView, ExpensePartialUpdateView, ExpenseDeleteView, AccountTypeListAPIView, AccountTypeCreateAPIView, AccountTypeRetrieveAPIView, AccountTypeUpdateAPIView, AccountTypeDeleteAPIView, IncomesTypeListAPIView, IncomesTypeCreateAPIView, IncomesTypeRetrieveAPIView, IncomesTypeUpdateAPIView, IncomesTypeDeleteAPIView, ExpensesTypeListAPIView, ExpensesTypeCreateAPIView, ExpensesTypeRetrieveAPIView, ExpensesTypeUpdateAPIView, ExpensesTypeDeleteAPIView

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

    path('expenses_create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses_list/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses_update/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses_partial_update/<int:pk>/partial-update/', ExpensePartialUpdateView.as_view(), name='expense-partial-update'),
    path('expenses_delete/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),

    path('account_types_list/', AccountTypeListAPIView.as_view(), name='account-types-list'),
    path('account_types_create/', AccountTypeCreateAPIView.as_view(), name='account-types-create'),
    path('account_types_detail/<int:pk>/', AccountTypeRetrieveAPIView.as_view(), name='account-types-detail'),
    path('account_types_update/<int:pk>/update/', AccountTypeUpdateAPIView.as_view(), name='account-types-update'),
    path('account_types_delete/<int:pk>/delete/', AccountTypeDeleteAPIView.as_view(), name='account-types-delete'),

    path('incomes_types_list/', IncomesTypeListAPIView.as_view(), name='incomes-types-list'),
    path('incomes_types_create/', IncomesTypeCreateAPIView.as_view(), name='incomes-types-create'),
    path('incomes_types_detail/<int:pk>/', IncomesTypeRetrieveAPIView.as_view(), name='incomes-types-detail'),
    path('incomes_types_update/<int:pk>/update/', IncomesTypeUpdateAPIView.as_view(), name='incomes-types-update'),
    path('incomes_types_delete/<int:pk>/delete/', IncomesTypeDeleteAPIView.as_view(), name='incomes-types-delete'),

    path('expenses_types_list/', ExpensesTypeListAPIView.as_view(), name='expenses-types-list'),
    path('expenses_types_create/', ExpensesTypeCreateAPIView.as_view(), name='expenses-types-create'),
    path('expenses_types_detail/<int:pk>/', ExpensesTypeRetrieveAPIView.as_view(), name='expenses-types-detail'),
    path('expenses_types_update/<int:pk>/update/', ExpensesTypeUpdateAPIView.as_view(), name='expenses-types-update'),
    path('expenses_types_delete/<int:pk>/delete/', ExpensesTypeDeleteAPIView.as_view(), name='expenses-types-delete'),
]