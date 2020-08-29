from django.contrib import admin
from django.contrib.auth.models import User
from .models import Place, Camping, Note

admin.site.register(Camping)
admin.site.register(Place)
admin.site.register(Note)


# Register your models here.
