from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from devices.models import Building, Inventory,Room,InventorizationList,Device
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
        try:

            building_id = data.get('inventory_id')
            inventory = Inventory.objects.get(id = building_id)
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



            # Create new InventorizationList
            inventory_list = InventorizationList.objects.create(
                inventory = inventory,
                creator=request.user,  # Use the authenticated user
                building=building,
                status='ACTIVE',
                start_date=timezone.now()
            )

            return JsonResponse({'success': True, 'message': 'Inventory started successfully','inventory_id':inventory.id, 'inventory_list_id': inventory_list.id,})

        except Building.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid building'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'You do not have permission to perform this action. You are not an inventory manager.'})

@login_required
@require_POST
def update_inventory_room_data(request, inventory_id):
    if not is_inventory_manager(request.user):
        return JsonResponse({'success': False, 'message': 'You do not have permission to perform this action. You are not an inventory manager.'})
    
    inventory = get_object_or_404(InventorizationList, id=inventory_id)
    if inventory.status in ['ACTIVE', 'PAUSED']:
        inventory.initialize_inventory_data()
        return JsonResponse({'success': True, 'message': 'Room data updated successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Inventory is not active or paused'})


@login_required
@user_passes_test(is_inventory_manager)
def edit_inventory(request):
    # This view should render a page or form for editing the current inventory
    # It's not an API endpoint, so it should return a rendered HTML page
    context = {}  # Replace with your actual context data
    return render(request, 'devices/edit_inventory.html', context)

@require_POST
@login_required(login_url='login')
def pause_resume_inventory(request):

    if not is_inventory_manager(request.user):
        return JsonResponse({'success': False, 'message': 'You do not have permission to perform this action. You are not an inventory manager.'})

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
@login_required
def end_inventory(request):
    data = json.loads(request.body)
    inventory_id = data.get('inventory_id')
    inventorization = get_object_or_404(InventorizationList, id=inventory_id)
    
    if inventorization.status in ['ACTIVE', 'PAUSED']:
        inventorization.end_inventory_list()
        return JsonResponse({
            'status': 'success',
            'message': 'Inventory completed successfully',
            'file_url': inventorization.inventory_data_file.url
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'This inventory is already completed or canceled'
        }, status=400)

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
    
@login_required(login_url='login')
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
    

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Device, IoTDevice, IoTDeviceEndpoint

@login_required(login_url='login')
@require_http_methods(["GET"])
def get_iot_settings(request, device_id):
    try:
        device = Device.objects.get(id=device_id)
        iot_device = IoTDevice.objects.get(device=device)
        
        endpoints = [
            {
                'name': endpoint.name,
                'url': endpoint.url
            }
            for endpoint in IoTDeviceEndpoint.objects.filter(device=iot_device)
        ]
        
        return JsonResponse({
            'success': True,
            'ipAddress': iot_device.ip_address,
            'token': iot_device.token,
            'endpoints': endpoints
        })
    except (Device.DoesNotExist, IoTDevice.DoesNotExist):
        return JsonResponse({
            'success': False,
            'error': 'IoT device not found'
        }, status=404)

@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_iot_features(request):
    data = json.loads(request.body)
    device_id = data.get('deviceId')

    try:
        device = Device.objects.get(id=device_id)
        iot_device = IoTDevice.objects.get(device=device)
        
        IoTDeviceEndpoint.objects.filter(device=iot_device).delete()
        iot_device.delete()

        return JsonResponse({'success': True})
    except (Device.DoesNotExist, IoTDevice.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'IoT device not found'}, status=404)
    
@login_required
@require_http_methods(["POST"])
def activate_iot_features(request):
    data = json.loads(request.body)
    device_id = data.get('deviceId')
    ip_address = data.get('ipAddress')
    token = data.get('token')

    try:
        device = Device.objects.get(id=device_id)
        
        # Check if the IP address is already in use
        if IoTDevice.objects.filter(ip_address=ip_address).exists():
            return JsonResponse({'success': False, 'error': 'This IP address is already in use by another IoT device'}, status=400)

        iot_device, created = IoTDevice.objects.get_or_create(
            device=device,
            defaults={'ip_address': ip_address, 'token': token}
        )
        if not created:
            iot_device.ip_address = ip_address
            iot_device.token = token
            iot_device.save()

        # Create default 'status' endpoint
        IoTDeviceEndpoint.objects.get_or_create(
            device=iot_device,
            name='status',
            defaults={'url': f'http://{ip_address}/api/status'}
        )

        return JsonResponse({'success': True})
    except Device.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Device not found'}, status=404)


@login_required
@require_http_methods(["POST"])
def check_and_update_iot_device(request):
    data = json.loads(request.body)
    device_id = data.get('deviceId')
    ip_address = data.get('ipAddress')
    token = data.get('token')


    
    try:
        device = Device.objects.get(id=device_id)
        iot_device = IoTDevice.objects.get(device=device)
        status_endpoint = iot_device.endpoints.filter(name='status').first().url
    except IoTDevice.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Device not found'}, status=404)

    # Check device status
    try:
        response = requests.get(f"http://{ip_address}/{status_endpoint}?token={token}", 
                                headers={'Authorization': f'Token {token}', 'X-IoTDeviceToken': token},
                                timeout=5)
        
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'success': False, 'error': f'Failed to connect to device: {str(e)}'}, status=400)

    # Update the device settings

    
    iot_device.ip_address = ip_address
    iot_device.token = token
    iot_device.save()

    return JsonResponse({'success': True, 'message': 'Device checked and settings updated successfully'})

@login_required
@require_http_methods(["POST"])
def led_control(request, device_id):


    try :
        iotDevice = IoTDevice.objects.get(id=device_id)
        data = json.loads(request.body)

        url = f"http://{iotDevice.ip_address}/api/leds"
        params = {
            'token': iotDevice.token,
        }
        
        if (data['pattern']): 
            params['pattern'] = data['pattern']
            if(data['interval']):
                params['interval'] = data['interval']
        
        
        response = requests.get(url, params=params)
        
        return JsonResponse({'success': True,'response':response.json(), 'message': 'LED control request sent successfully'})
    except IoTDevice.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def save_iot_device_state(request, device_id):
    try:
        iot_device = IoTDevice.objects.get(id=device_id)
        
        url=f"http://{iot_device.ip_address}/api/save_state"
        params = {
             'token' : iot_device.token
        }
        # Make a request to the IoT device to save its state
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return JsonResponse({'status': 'ok', 'message': 'State saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to save state on device'}, status=500)
    
    except IoTDevice.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Device not found'}, status=404)
    except requests.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Error communicating with device: {str(e)}'}, status=500)
