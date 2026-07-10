from django.urls import path

from biller_apps.overview_report.controller import OverviewReportViewController

urlpatterns = [
    path('get_customer_overview_reports/', OverviewReportViewController.get_customer_overview_reports, name='get_customer_overview_reports'),
    path('get_item_overview_reports/', OverviewReportViewController.get_overview_reports, name='get_item_overview_reports'),
    path('get_supplier_overview_reports/', OverviewReportViewController.get_supplier_overview_reports, name='get_supplier_overview_reports'),
    path('download-overview-report/', OverviewReportViewController.download_overview_report, name='download-overview-report'),

]
