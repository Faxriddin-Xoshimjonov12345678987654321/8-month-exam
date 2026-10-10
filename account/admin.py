from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(ProfileUser)
admin.site.register(Hisob)
admin.site.register(Kirimlar)
admin.site.register(Chiqimlar)
admin.site.register(Verify)