from django.contrib import admin
from .models import *

admin.site.register(SuperAdmin)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Visitor)
