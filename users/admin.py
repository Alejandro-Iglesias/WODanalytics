from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Panel de administración personalizado para el modelo User.
    """

    list_display = ["username", "email", "fecha_registro", "is_staff"]
    search_fields = ["username", "email"]
