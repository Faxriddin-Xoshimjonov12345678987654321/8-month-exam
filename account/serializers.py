from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from base.utils import send_eemail_code, email_phone_regex, validate_username

from .models import ProfileUser, Hisob, Kirimlar, Chiqimlar, VIA_EMAIL, VIA_PHONE, DONE, PHOTO_DONE

class SignUpSerializer(serializers.ModelSerializer):
    email_or_phone_number = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = ProfileUser
        fields = ['id', 'username', 'auth_type', 'auth_status', 'email_or_phone_number']
        read_only_fields = ['id', 'auth_type', 'auth_status']


    def validate_username(self, value):
        return validate_username(value)


    def validate(self, attrs):
        user_input = attrs.get('email_or_phone_number')
        username = attrs.get('username')

        user = ProfileUser.objects.filter(Q(phone_number=user_input) | Q(email=user_input)).first()

        if user:
            if user.auth_status in [DONE, PHOTO_DONE]:
                raise ValidationError('email yoki telefon raqamingiz bizda oldin royxatdan otgan')
            else:
                user.delete()

        user_input_tupe = email_phone_regex(user_input)

        if user_input_tupe == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL, 
                'username': username
            }

        elif user_input_tupe == 'phone':
            data = {
                'phone': user_input,
                'auth_type': VIA_PHONE,
                'username': username

            }

        else:
            raise ValidationError('Siz xato email yoki telefon raqam kiritingiz')

        return data

    
    def create(self, validated_data):
        user = ProfileUser(**validated_data)
        user.save()

        if user.auth_type == VIA_EMAIL:
            code = user.generate_code(user.auth_type)
            print(f"EMAIL CODE: {code}")

            is_sent = send_eemail_code(user.email, code)
            if not is_sent:
                raise ValidationError('Tasdiqlash kodini yuborishda xatolik yuz berdi Emailni tekshiring')

        elif user.auth_type ==VIA_PHONE:
            code = user.generate_code(user.auth_type)
            print(f"PHONE NUMBER CODE: {code}")
            # ....

        else:
            raise ValidationError('Email yoki telefon xato kiritilgan')

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return {
            'token':instance.token(),
            'data': data
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = ProfileUser
        fields = ['username', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if not password or not confirm_password:
            raise ValidationError('Parol va tasdiqlash paroli kiritilishi shart!')

        if password != confirm_password:
            raise ValidationError('Parollar mos emas')

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance



class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, required=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisob
        fields = ['id', 'name', 'balance', 'currency', 'created_at', 'update_at']
        read_only_fields = ['id', 'created_at', 'update_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kirimlar
        fields = ['id', 'account', 'title', 'amount', 'description', 'created_at', 'update_at']
        read_only_fields = ['id', 'created_at', 'update_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chiqimlar
        fields = ['id', 'account', 'title', 'amount', 'description', 'created_at', 'update_at']
        read_only_fields = ['id', 'created_at', 'update_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
        