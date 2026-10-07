from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

import uuid
import random

# Create your models here.


NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
ADMIN, USER = ('admin', 'user')


class ProfileUser(AbstractUser):
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE),
    )

    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )

    AUTH_ROLE = (
        (ADMIN, ADMIN),
        (USER, USER),
    )

    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=30, choices=AUTH_TYPE, blank=True, null=True)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE, default=USER)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    addres = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.username

    def check_username(self):
        if not self.username:
            ud = str(uuid.uuid4())
            temp_username = f"username{ud[ud.rfind('-'):]}"

            while ProfileUser.objects.filter(username=temp_username).exists():
                temp_username += str(random.randint(0,10))
                
            self.username = temp_username

    def check_pass(self):
        if not self.password:
            ud = str(uuid.uuid4())
            temp_password = f"password{ud[ud.rfind('-'):]}"
            self.password = temp_password

    def hashing_pass(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def email_normalize(self):
        if self.email:
            temp_email = self.email.lower()
            self.email = temp_email

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def save(self, *args, **kwargs):
        self.check_username()
        self.check_pass()
        self.hashing_pass()
        self.email_normalize()
        return super().save(*args, **kwargs)
        