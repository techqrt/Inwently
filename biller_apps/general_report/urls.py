from django.urls import path

from biller_apps.general_report.controller import GeneralReportViewController

urlpatterns = [
    path('get_purchase_reports/', GeneralReportViewController.get_purchase_reports, name='get_purchase_reports'),
    path('get_quotation_reports/', GeneralReportViewController.get_quotation_reports, name='get_quotation_reports'),
]
