from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from .serializers import SignUpSerializer, VerifySerializer, AccountSerializer, IncomeSerializer, ExpenseSerializer, UpdateUserSerializer, AccountTypeSerializer, IncomesTypeSerializer, ExpensesTypeSerializer, HisoblarSerializer
from .models import ProfileUser, Verify, NEW, DONE, Kirimlar, Chiqimlar, Hisob, HisobTurlari, KirimTurlari, ChiqimlarTurlar, Hisoblar
from datetime import datetime
# Create your views here.

class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    queryset = ProfileUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class VerifyView(GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        user = request.user

        verifies = Verify.objects.filter(user=user, code=code, used=False, expire_time__gte=datetime.now())

        if not verifies.exists():
            raise ValidationError('Tasdiqlash kodi xato yoki yaroqsiz')

        verify = verifies.first()
        verify.used = True
        verify.save()  

        if user.auth_status == NEW:
            user.auth_status = DONE
            user.save()

        return Response({
            'message': 'Kod muvaffaqiyatli tasdiqlandi!',
            'auth_status': user.auth_status
        })


class UpdateUserView(GenericAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, reqeust):
        user = reqeust.user 
        serializer = self.get_serializer(user, data=reqeust.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response({
                'message': 'Siz muvaffaqaiyatli royxatdan otdingiz',
                'auth_status': user.auth_status
        })


class AccountCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AccountList(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Hisob.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request):
        accounts = self.get_queryset()
        serializer = self.get_serializer(accounts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class IncomeCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
        

class IncomeListView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeSerializer
    queryset = Kirimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request):
        incomes = self.get_queryset()
        serializer = self.get_serializer(incomes, many=True)

        return Response(serializer.data)


class IncomeUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeSerializer
    queryset = Kirimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def put(self, request, pk):
        income = self.get_object()

        serializer = self.get_serializer(income, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class IncomePartialUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeSerializer
    queryset = Kirimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def patch(self, request, pk):
        income = self.get_object()

        serializer = self.get_serializer(income, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class IncomeDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Kirimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def delete(self, request):
        income = self.get_object()

        income.delete()

        return Response({}, status=status.HTTP_200_OK)


class ExpenseCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ExpenseListView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer
    queryset  = Chiqimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request):
        expenses = self.get_queryset()
        serializer = self.get_serializer(expenses, many=True)

        return Response(serializer.data)


class ExpenseUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer
    queryset = Chiqimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def put(self, request, pk):
        expense = self.get_object()
        serializer = self.get_serializer(instance=expense, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    
class ExpensePartialUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer
    queryset = Chiqimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def patch(self, request, pk):
        expense = self.get_object()
        serializer = self.get_serializer(instance=expense, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ExpenseDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Chiqimlar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def delete(self, request, pk):
        expense = self.get_object()

        expense.delete()

        return Response({}, status=status.HTTP_200_OK)


class AccountTypeListAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = AccountTypeSerializer
  queryset = HisobTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request):
    account_types = self.get_queryset()
    serializer = self.get_serializer(account_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AccountTypeCreateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = AccountTypeSerializer

  def post(self, request):
    serializer = self.get_serializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountTypeRetrieveAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = AccountTypeSerializer
  queryset = HisobTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request, pk=None):
    account_type = self.get_object()
    serializer = self.get_serializer(account_type)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AccountTypeUpdateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = AccountTypeSerializer
  queryset = HisobTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def put(self, request, pk=None):
    account_type = self.get_object()
    serializer = self.get_serializer(
        account_type, data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class AccountTypeDeleteAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = HisobTurlari.objects.all()
  serializer_class = AccountTypeSerializer

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def delete(self, request, pk=None):
    account_type = self.get_object()
    account_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class IncomesTypeListAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = IncomesTypeSerializer
  queryset = KirimTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request):
    incomes_types = self.get_queryset()
    serializer = self.get_serializer(incomes_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class IncomesTypeCreateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = IncomesTypeSerializer

  def post(self, request):
    serializer = self.get_serializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncomesTypeRetrieveAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = IncomesTypeSerializer
  queryset = KirimTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request, pk=None):
    incomes_type = self.get_object()
    serializer = self.get_serializer(incomes_type)
    return Response(serializer.data, status=status.HTTP_200_OK)


class IncomesTypeUpdateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = IncomesTypeSerializer
  queryset = KirimTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def put(self, request, pk=None):
    incomes_type = self.get_object()
    serializer = self.get_serializer(
        incomes_type, data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class IncomesTypeDeleteAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = KirimTurlari.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def delete(self, request, pk=None):
    incomes_type = self.get_object()
    incomes_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ExpensesTypeListAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ExpensesTypeSerializer
  queryset = ChiqimlarTurlar.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request):
    expenses_types = self.get_queryset()
    serializer = self.get_serializer(expenses_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ExpensesTypeCreateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ExpensesTypeSerializer

  def post(self, request):
    serializer = self.get_serializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpensesTypeRetrieveAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ExpensesTypeSerializer
  queryset = ChiqimlarTurlar.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def get(self, request, pk=None):
    expenses_type = self.get_object()
    serializer = self.get_serializer(expenses_type)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ExpensesTypeUpdateAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ExpensesTypeSerializer
  queryset = ChiqimlarTurlar.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def put(self, request, pk=None):
    expenses_type = self.get_object()
    serializer = self.get_serializer(
        expenses_type, data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class ExpensesTypeDeleteAPIView(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = ChiqimlarTurlar.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def delete(self, request, pk=None):
    expenses_type = self.get_object()
    expenses_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class HisoblarListAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HisoblarSerializer
    queryset = Hisoblar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request):
        hisoblar = self.get_queryset()
        serializer = self.get_serializer(hisoblar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HisoblarCreateAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HisoblarSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HisoblarRetrieveAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HisoblarSerializer
    queryset = Hisoblar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, pk=None):
        hisob = self.get_object()
        serializer = self.get_serializer(hisob)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HisoblarUpdateAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HisoblarSerializer
    queryset = Hisoblar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def put(self, request, pk=None):
        hisob = self.get_object()
        serializer = self.get_serializer(hisob, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HisoblarDeleteAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hisoblar.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def delete(self, request, pk=None):
        hisob = self.get_object()
        hisob.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DashboardAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        total_balance = Hisoblar.objects.filter(user=user).aggregate(sum=Sum('balance'))['sum'] or 0.00
        total_income = Kirimlar.objects.filter(user=user).aggregate(sum=Sum('amount'))['sum'] or 0.00
        total_expense = Chiqimlar.objects.filter(user=user).aggregate(sum=Sum('amount'))['sum'] or 0.00
        
        data = {
            'total_balance': total_balance,
            'total_income': total_income,
            'total_expense': total_expense
        }
        return Response(data, status=status.HTTP_200_OK)