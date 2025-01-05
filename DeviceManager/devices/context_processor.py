from django.contrib.auth.models import Group

def group_membership(request):
    return {
        'is_inventory_manager': request.user.groups.filter(name='Inventory-Managers').exists()
    }