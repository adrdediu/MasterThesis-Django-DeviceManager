from django.contrib import admin
from .models import DeviceScan,ExtendedUser,Building, Floor, Inventory, InventoryChange, IoTDeviceResponse, Room, Device,Category,Subcategory,InventorizationList,IoTDevice,IoTDeviceEndpoint



admin.site.register(ExtendedUser)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Inventory)
admin.site.register(InventoryChange)
admin.site.register(DeviceScan)
admin.site.register(InventorizationList)
admin.site.register(IoTDevice)
admin.site.register(IoTDeviceEndpoint)
admin.site.register(IoTDeviceResponse)

