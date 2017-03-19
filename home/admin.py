from django.contrib import admin
from home.models import Users,Grade,Constants
from calculation.models import Result
# Register your models here.

admin.site.register(Users)
admin.site.register(Grade)
admin.site.register(Constants)
admin.site.register(Result)