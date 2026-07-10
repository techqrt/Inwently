from django.urls import path

from biller_apps.admin_report.controller import AdminReportViewController

urlpatterns = [
    path('get_admin_reports/', AdminReportViewController.get_admin_reports, name='get_admin_reports'),
]