# devices/urls.py

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from devices.views import  DeviceDetailView, add_device, GetFloorsView, GetRoomsView, GetSubcategoriesView
from devices.views import DownloadQRCodeView, HomePageView, DeviceListView
from devices.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomePageView.as_view(), name='homepage'),
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/<str:category>/', DeviceListView.as_view(), name='device_list_with_category'),
    path('devices/<str:category>/<str:subcategory>/', DeviceListView.as_view(), name='device_list_with_subcategory'),
    path('add_device/', add_device, name='add_device'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('get_floors/', GetFloorsView.as_view(), name='get_floors'),
    path('get_rooms/', GetRoomsView.as_view(), name='get_rooms'),
    path('get_subcategories/',GetSubcategoriesView.as_view(),name='get_subcategories'),
    path('download_qrcode/<int:device_id>/', DownloadQRCodeView.as_view(), name='download_qrcode'),
    # Add other URL patterns as needed
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)