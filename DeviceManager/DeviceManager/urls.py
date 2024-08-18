# devices/urls.py

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,re_path
from devices.sse_views import SSEDeviceUpdateView
from devices.views import  DeviceDetailView, add_device,edit_device, delete_device, update_profile, change_password
from devices.views import GetFloorsView, GetRoomsView, GetSubcategoriesView,InventorizationListDetailView
from devices.views import DownloadQRCodeView, HomePageView, DeviceListView
from devices.views import LoginView, LogoutView,InventoryManagementView, generate_inventory_report_view
from devices.api_views import activate_iot_features,led_control, remove_iot_features, start_inventory, pause_resume_inventory, end_inventory, edit_inventory,cancel_inventory,qrcode_action, update_inventory_room_data,get_iot_settings, check_and_update_iot_device, save_iot_device_state 
from devices.views import NextJSView,DashboardView
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls),
    path('update_profile/', update_profile, name='update_profile'),
    path('change_password/', change_password, name='change_password'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='homepage'),
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/<str:category>/', DeviceListView.as_view(), name='device_list_with_category'),
    path('devices/<str:category>/<str:subcategory>/', DeviceListView.as_view(), name='device_list_with_subcategory'),
    path('api/devices/add_device/', add_device, name='add_device'),
    path('api/devices/edit/', edit_device, name='edit_device'),
    path('api/devices/delete_device/', delete_device, name='delete_device'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),

    path('get_floors/', GetFloorsView.as_view(), name='get_floors'),
    path('get_rooms/', GetRoomsView.as_view(), name='get_rooms'),
    path('get_subcategories/',GetSubcategoriesView.as_view(),name='get_subcategories'),
    path('download_qrcode/<int:device_id>/', DownloadQRCodeView.as_view(), name='download_qrcode'),
    # Add other URL patterns as needed
    path('api/device/<int:device_id>/qrcode/<str:action>/', qrcode_action, name='qrcode_action'),
    path('api/inventory/<int:inventory_id>/generate-report/', generate_inventory_report_view, name='generate_inventory_report'),
    
    path('inventory/management/<int:pk>/', InventoryManagementView.as_view(), name='inventory_management'),
    path('inventory/cancel/', cancel_inventory, name='api_cancel_inventory'),
    path('inventory/start/', start_inventory, name='api_start_inventory'),
    path('inventory/update_inventory_room_data/<int:inventory_id>/', update_inventory_room_data, name='update_inventory_room_data'),
    path('inventory/pause-resume/', pause_resume_inventory, name='api_pause_resume_inventory'),
    path('inventory/end/', end_inventory, name='api_end_inventory'),
    path('inventory/edit/', edit_inventory, name='api_edit_inventory'),
    path('inventory/<int:pk>/', InventorizationListDetailView.as_view(), name='inventory_detail'),

    # Add Paths used for IoT View
    path('api/activate_iot_features/', activate_iot_features, name='activate_iot_features'),
    path('api/get_iot_settings/<int:device_id>/',get_iot_settings, name='get_iot_settings'),
    path('api/update_iot_settings/', check_and_update_iot_device, name='update_iot_settings'),
    path('api/remove_iot_features/', remove_iot_features, name='remove_iot_features'),
    path('api/iot_device/<int:device_id>/setleds/',led_control, name='led_control'),
    path('api/iot_device/<int:device_id>/save_state/', save_iot_device_state, name='save_iot_device_state'),


    path('nextjs/', NextJSView.as_view(), name='nextjs'),
    path('nextjs/dashboard/', DashboardView.as_view(), name='dashboard'),

    # Add Paths used for SSE
     path('sse/<int:device_id>/', SSEDeviceUpdateView.as_view(), name='sse_device_updates'),
    
    # Add this new pattern to serve Static NextJS Files
    re_path(r'^nextjs/static/(?P<path>.*)$', serve, {
        'document_root': settings.STATICFILES_DIRS[0]
    }),]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)