from django.contrib import admin
from .models import Building, Floor, Room, Device,Category,Subcategory,InventorizationDevice,InventorizationList,InventorizationRoom

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(InventorizationDevice)
admin.site.register(InventorizationList)
admin.site.register(InventorizationRoom)
