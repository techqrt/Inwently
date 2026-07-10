from django.urls import path

from biller_apps.auth.controller import AuthController

urlpatterns = [
    path('login/', AuthController.login, name='login'),
    path('token/', AuthController.get_token, name='token'),
    path('register/', AuthController.register, name='activate'),
    path('password_change/', AuthController.password_change, name='password_change'),
    path('forgot_password/', AuthController.forgot_password, name='forgot_password'),
    path('email_verify/', AuthController.email_verify, name='email_verify'),

]
