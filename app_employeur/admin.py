from django.contrib import admin
from .models import *

@admin.register(Employeur)
class EmployeurAdmin(admin.ModelAdmin):
   pass 
    