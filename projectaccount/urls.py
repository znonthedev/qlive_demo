from django.urls import path
from rest_framework_nested import routers
from .views import (
    LoginView,
    RegisterUserView,
    UpdateStaffPasswordView,
    LogoutView,
    PasswordResetView,
    PasswordConfirmView,
    OTPConfirmationView
)



urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/staff/", RegisterUserView.as_view(), name="register"),
    path("staff/<int:pk>/", RegisterUserView.as_view(), name="user-detail"),
    path("staff/update-password/<int:pk>/", UpdateStaffPasswordView.as_view(), name="update-password"),
    path("resetpassword/", PasswordResetView.as_view(), name="resetpassword"),
    path("confirmpassword/", PasswordConfirmView.as_view(), name="resetpassword"),
    path("confirmotp/", OTPConfirmationView.as_view(), name="confirmotp"),
]


router = routers.DefaultRouter()

urlpatterns = router.urls + urlpatterns
