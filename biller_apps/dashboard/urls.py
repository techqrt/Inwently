from django.urls import path

from biller_apps.dashboard.controller import DashboardController

urlpatterns = [
    path('web_count/', DashboardController.web_count, name='dashboard_web_count'),
]
