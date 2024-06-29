from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from devices.models import Building,Room,InventorizationList,Device
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils import timezone
import json

def is_inventory_manager(user):
    """
    Check if the user belongs to the 'inventory-managers' group.
    """
    if user.is_authenticated and user.groups.filter(name='Inventory-Managers').exists():
        return True
    else:
        return False

@require_POST
@login_required(login_url='login')
def start_inventory(request):
    
    if is_inventory_manager(request.user):
        data = json.loads(request.body)
        building_id = data.get('building_id')
        room_ids = data.get('room_ids', [])
        scope = data.get('scope') 
        
        # Handle Scope
        if scope not in ['ENTIRE', 'PARTIAL']:
            return JsonResponse({'success': False, 'message': 'Invalid scope'})

        try:
            building = Building.objects.get(id=building_id)

            # Check if there's an active inventory for this building
            active_inventory = InventorizationList.objects.filter(
                Q(building=building) & 
                (Q(status='ACTIVE') | Q(status='PAUSED'))
            ).first()

            if active_inventory:
                return JsonResponse({
                    'success': False, 
                    'message': f'An active inventory (ID: {active_inventory.id}) already exists for this building. Please complete or cancel it before starting a new one.'
                })

            if room_ids == 'all':
                # If 'all' is received, get all room IDs for the building
                room_ids = list(Room.objects.filter(building=building).values_list('id', flat=True))
            else:
                # Ensure room_ids is a list of integers
                room_ids = [int(id) for id in room_ids]
                # Verify that all provided room IDs belong to the selected building
                valid_room_ids = set(Room.objects.filter(building=building, id__in=room_ids).values_list('id', flat=True))
                room_ids = list(valid_room_ids)

            if not room_ids:
                return JsonResponse({'success': False, 'message': 'No valid rooms selected'})

            # Create new InventorizationList
            inventory = InventorizationList.objects.create(
                creator=request.user,  # Use the authenticated user
                building=building,
                room_ids=room_ids,
                status='ACTIVE',
                scope=scope,
                start_date=timezone.now()
            )

            return JsonResponse({'success': True, 'message': 'Inventory started successfully', 'inventory_id': inventory.id})

        except Building.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid building'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'You do not have permission to perform this action. You are not an inventory manager.'})



@login_required
@user_passes_test(is_inventory_manager)
def edit_inventory(request):
    # This view should render a page or form for editing the current inventory
    # It's not an API endpoint, so it should return a rendered HTML page
    context = {}  # Replace with your actual context data
    return render(request, 'devices/edit_inventory.html', context)

@login_required
@user_passes_test(is_inventory_manager)
@require_GET
def get_inventory_status(request):
    current_inventory = Inventory.objects.filter(status__in=['active', 'paused']).first()
    if current_inventory:
        return JsonResponse({
            'success': True,
            'status': current_inventory.status,
            'started_at': current_inventory.created_at.isoformat(),
            'id': current_inventory.id
        })
    return JsonResponse({'success': False, 'message': 'No active inventory found'})

@require_POST
@login_required(login_url='login')
def pause_resume_inventory(request):
    data = json.loads(request.body)
    inventory_id = data.get('inventory_id')
    action = data.get('action')

    try:
        inventory = InventorizationList.objects.get(id=inventory_id)
        # Handle Browser Override
        if inventory.status == 'COMPLETED' or inventory.status == 'CANCELLED':
            return JsonResponse({'success': False, 'message': 'Inventory has already been completed/cancelled'})
        
        if action == 'pause':
            inventory.status = 'PAUSED'
        elif action == 'resume':
            inventory.status = 'ACTIVE'
        inventory.save()
        return JsonResponse({'success': True, 'message': f'Inventory {action}d successfully'})
    except InventorizationList.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inventory not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
@login_required(login_url='login')
def end_inventory(request):
    data = json.loads(request.body)
    inventory_id = data.get('inventory_id')

    try:
        inventory = InventorizationList.objects.get(id=inventory_id)
        if inventory.status == 'CANCELED':
            return JsonResponse({'success': False, 'message': 'Inventory already ended'})
        else:
            inventory.status = 'COMPLETED'
            inventory.end_date = timezone.now()
            inventory.save()
            return JsonResponse({'success': True, 'message': 'Inventory ended successfully'})
    except InventorizationList.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inventory not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
@login_required(login_url='login')
def cancel_inventory(request):
    data = json.loads(request.body)
    inventory_id = data.get('inventory_id')

    try:
        inventory = InventorizationList.objects.get(id=inventory_id)
        inventory.status = 'CANCELED'
        inventory.end_date = timezone.now()
        inventory.save()
        return JsonResponse({'success': True, 'message': 'Inventory canceled successfully'})
    except InventorizationList.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inventory not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@login_required
@require_POST
def qrcode_action(request, device_id, action):
    try:
        device = Device.objects.get(pk=device_id)
        if action == 'regenerate':
            device.regenerate_qr_code()
        elif action == 'generate':
            device.generate_qr_code()
        return JsonResponse({'success': True})
    except Device.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Device not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
