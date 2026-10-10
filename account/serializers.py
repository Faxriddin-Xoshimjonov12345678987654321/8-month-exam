from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from base.utils import send_eemail_code, email_phone_regex, validate_username

from .models import ProfileUser, VIA_EMAIL, VIA_PHONE, DONE, PHOTO_DONE

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
                'auth_type': VIA_EMAIL
            }

        elif user_input_tupe == 'phone':
            data = {
                'phone': user_input,
                'auth_type': VIA_PHONE
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


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_leng=4, required=True)