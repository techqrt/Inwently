from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('organisation/', include('biller_apps.organisation.urls')),
    path('auth/', include('biller_apps.auth.urls')),
    path('employees/', include('biller_apps.employees.urls')),
    path('shops/', include('biller_apps.shops.urls')),
    path('dashboard/', include('biller_apps.dashboard.urls')),
    path('item/', include('biller_apps.item.urls')),
    path('supplier/', include('biller_apps.supplier.urls')),
    path('brand/', include('biller_apps.brand.urls')),
    path('category/', include('biller_apps.category.urls')),
    path('status/', include('biller_apps.status.urls')),
    path('billing/', include('biller_apps.billing.urls')),
    path('places/', include('biller_apps.places.urls')),
    path('storage/', include('biller_apps.storage.urls')),
    path('customer/', include('biller_apps.customer.urls')),
    path('approvals/', include('biller_apps.approvals.urls')),
    path('taxes/', include('biller_apps.taxes.urls')),
    path('purchase/', include('biller_apps.purchase.urls')),
    path('return-purchase/', include('biller_apps.return_purchase.urls')),
    path('stock-transfer/', include('biller_apps.stock_transfer.urls')),
    path('return-item/', include('biller_apps.return_item.urls')),
    path('quotations/', include('biller_apps.quotations.urls')),
    path('pos/', include('biller_apps.pos.urls')),
    path('inventory/', include('biller_apps.inventory.urls')),
    path('general-report/', include('biller_apps.general_report.urls')),
    path('overview-report/', include('biller_apps.overview_report.urls')),
    path('admin-report/', include('biller_apps.admin_report.urls')),
    path('customer-quotation/', include('biller_apps.customer_quotation.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
