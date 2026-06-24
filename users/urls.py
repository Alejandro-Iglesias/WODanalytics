from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    path("register/", view=RegisterView.as_view(), name="register"),
    path("profile/", view=UserProfileView.as_view(), name="profile"),
]
