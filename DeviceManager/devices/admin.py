from django.contrib import admin
from .models import ExtendedUser,Building, Floor, Inventory, InventoryChange, Room, Device,Category,Subcategory,InventorizationList



admin.site.register(ExtendedUser)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Inventory)
admin.site.register(InventoryChange)
admin.site.register(InventorizationList)

