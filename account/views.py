from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .serializers import SignUpSerializer, VerifySerializer, AccountSerializer, IncomeSerializer, ExpenseSerializer, UpdateUserSerializer
from .models import ProfileUser, Verify, NEW, DONE, Kirimlar, Chiqimlar, Hisob
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