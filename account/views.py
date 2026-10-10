from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .serializers import SignUpSerializer, VerifySerializer, AccountSerializer, IncomeSerializer, ExpenseSerializer
from .models import ProfileUser, Verify, NEW, DONE
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

        verifies.first()
        verifies.used = True
        verifies.save()

        if user.auth_status == NEW:
            user.auth_status = DONE
            user.save()

        return Response({
            'message': 'Kod muvaffaqiyatli tasdiqlandi!',
            'auth_status': user.auth_status
        })


class AccountCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AccountList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = request.user.accounts.all()
        serializer = AccountSerializer(accounts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



    