from django.urls import path

from biller_apps.approvals.controller import ApprovalController

urlpatterns = [
    path('get_all_unapproved/', ApprovalController.get_all_unapproved, name='approval_get_all_unapproved'),
    path('status_change/', ApprovalController.status_change, name='approval_status_change'),
]
