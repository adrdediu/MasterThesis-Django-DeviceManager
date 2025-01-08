# devices/views.py
import requests
import json
import os
import datetime
from django.utils.timezone import now
from django.db.models import Max
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, FileResponse,HttpResponseBadRequest,HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm
from django.views.generic import DetailView, TemplateView
from .models import Device,Floor, Inventory, InventoryChange, IoTDevice,Room,Building,Subcategory,Category
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .utils import generate_inventory_excel_report,generate_inventory_pdf_report
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .api_views import is_inventory_manager, is_device_owner

class LoginView(View):
    template_name = 'devices/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page or any other logic you want
                return redirect('homepage')
            else:
                # Authentication failed
                form.add_error('username', 'Invalid credentials. Please try again.')
                form.add_error('password', 'Invalid credentials. Please try again.')

        # If form is not valid, or authentication failed, render the login page with errors
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    template_name = 'devices/logout.html'

    def post(self, request, *args, **kwargs):
        
        logout(request)

        return render(request, self.template_name)

class GetSubcategoriesView(LoginRequiredMixin,View):
    login_url = 'login'

    def get(self,request,*args,**kwargs):
        category_id = self.request.GET.get('category_id')
        subcategories = Subcategory.objects.filter(category__id=category_id)
        data =[{'id':subcategory.id,'name':subcategory.name} for subcategory in subcategories]

        return JsonResponse(data,safe=False)
    
class GetFloorsView(View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        building_id = self.request.GET.get('building_id')
        floors = Floor.objects.filter(building__id=building_id)
        data = [{'id': floor.id, 'name': floor.name} for floor in floors]
        return JsonResponse(data, safe=False)
    
class GetRoomsView(View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        floor_id = self.request.GET.get('floor_id')
        rooms = Room.objects.filter(floor_id=floor_id)
        data = [{'id': room.id, 'name': room.name} for room in rooms]
        return JsonResponse(data, safe=False)

class BaseContextMixin:
    def get_base_context(self):
        inventories = Inventory.objects.all()
        buildings = Building.objects.all()
        floors = Floor.objects.all()
        rooms = Room.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        return {
            'inventories': inventories,
            'buildings': buildings,
            'floors': floors,
            'rooms': rooms,
            'categories': categories,
            'subcategories': subcategories,
        }

class HomePageView(BaseContextMixin,LoginRequiredMixin,View):
    login_url = 'login'
    
    def get(self, request):
        context = self.get_base_context()
        return render(request, 'devices/home.html', context)

class DeviceListView(BaseContextMixin,LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, category=None, subcategory=None, building=None, floor=None, room=None):
        devices = Device.objects.all().filter(is_active=True).order_by('-id')

        context = self.get_base_context()
        context.update({
            'devices': devices,
        })

        return render(request, 'devices/device_list.html', context)

class DeletedDevicesListView(BaseContextMixin, LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        devices_query = Device.objects.filter(is_active=False)
        if 'my' in request.GET:
            devices_query = devices_query.filter(owner=request.user)
            title = 'My Deleted Devices'
            user_devices = True
        else:
            title = 'Deleted Devices'
            user_devices = False
            
        devices = devices_query.order_by('-id')
        
        context = self.get_base_context()
        context.update({
            'devices': devices,
            'deleted_devices': True,
            'user_devices': user_devices,
            'title': title
        })
        return render(request, 'devices/device_list.html', context)


class UserDevicesListView(BaseContextMixin,LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, category=None, subcategory=None, building=None, floor=None, room=None):
        devices = Device.objects.all().filter(owner=request.user,is_active=True).order_by('-id')

        context = self.get_base_context()
        context.update({
            'devices': devices,
            'user_devices': True,
        })

        return render(request, 'devices/device_list.html', context)

class CategoryDevicesListView(BaseContextMixin, LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        devices_query = Device.objects.filter(subcategory__category_id=category_id, is_active=True)
        
        if 'my' in request.GET:
            devices_query = devices_query.filter(owner=request.user)
            title_prefix = 'My '
            user_devices = True
        else:
            title_prefix = ''
            user_devices = False
            
        devices = devices_query.order_by('-id')
        category_subcategories = Subcategory.objects.filter(category=category)
        
        context = self.get_base_context()
        context.update({
            'devices': devices,
            'view_type': 'category',
            'current_category': category,
            'category_subcategories': category_subcategories,
            'title': f'{title_prefix}Devices in Category: {category.name}',
            'user_devices': user_devices
        })
        return render(request, 'devices/device_list.html', context)


class SubcategoryDevicesListView(BaseContextMixin, LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, subcategory_id):
        subcategory = Subcategory.objects.get(id=subcategory_id)
        devices_query = Device.objects.filter(subcategory_id=subcategory_id, is_active=True)
        
        if 'my' in request.GET:
            devices_query = devices_query.filter(owner=request.user)
            title_prefix = 'My '
            user_devices = True
        else:
            title_prefix = ''
            user_devices = False
            
        devices = devices_query.order_by('-id')
        
        context = self.get_base_context()
        context.update({
            'devices': devices,
            'view_type': 'subcategory',
            'current_subcategory': subcategory,
            'current_category': subcategory.category,
            'title': f'{title_prefix}Devices in Subcategory: {subcategory.name}',
            'user_devices': user_devices
        })
        return render(request, 'devices/device_list.html', context)


class BuildingDevicesListView(BaseContextMixin, LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, building_id):
        building = Building.objects.get(id=building_id)
        devices_query = Device.objects.filter(building_id=building_id, is_active=True)
        
        if 'my' in request.GET:
            devices_query = devices_query.filter(owner=request.user)
            title_prefix = 'My '
            user_devices = True
        else:
            title_prefix = ''
            user_devices = False
            
        devices = devices_query.order_by('-id')
        building_floors = Floor.objects.filter(building=building)
        
        context = self.get_base_context()
        context.update({
            'devices': devices,
            'view_type': 'building',
            'current_building': building,
            'building_floors': building_floors,
            'title': f'{title_prefix}Devices in Building: {building.acronym}',
            'user_devices': user_devices
        })
        return render(request, 'devices/device_list.html', context)

class RoomDevicesListView(BaseContextMixin, LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        devices_query = Device.objects.filter(room_id=room_id, is_active=True)
        
        if 'my' in request.GET:
            devices_query = devices_query.filter(owner=request.user)
            title_prefix = 'My '
            user_devices = True
        else:
            title_prefix = ''
            user_devices = False
            
        devices = devices_query.order_by('-id')
        
        context = self.get_base_context()
        context.update({
            'devices': devices,
            'view_type': 'room',
            'current_room': room,
            'current_building': room.building,
            'current_floor': room.floor,
            'title': f'{title_prefix}Devices in Room: {room.name}',
            'user_devices': user_devices
        })
        return render(request, 'devices/device_list.html', context)


@login_required
@require_POST
def update_profile(request):
    user = request.user
    password = request.POST.get('password')
    if not user.check_password(password):
        return JsonResponse({'success': False, 'message': 'Incorrect password'})
    
    # Validate email
    email = request.POST.get('email')
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'message': 'Invalid email address'})

    # Validate names
    first_name = request.POST.get('first_name').strip()
    last_name = request.POST.get('last_name').strip()
    if not first_name or not last_name:
        return JsonResponse({'success': False, 'message': 'First name and last name are required'})

    # Validate rank and faculty
    # admin_rank = request.POST.get('admin_rank')
    # rank = request.POST.get('rank')
    # faculty = request.POST.get('faculty')
    # if rank not in dict(user.extended_user.RANK_CHOICES):
    #     return JsonResponse({'success': False, 'message': 'Invalid rank selected'})
    # if admin_rank not in dict(user.extended_user.ADMIN_RANK_CHOICES):
    #     return JsonResponse({'success': False, 'message': 'Invalid admin rank selected'})
    # if faculty not in dict(user.extended_user.FACULTY_CHOICES):
    #     return JsonResponse({'success': False, 'message': 'Invalid faculty selected'})

    # Update user information
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    
    # Update extended user information
    extended_user = user.extended_user
    # extended_user.admin_rank = admin_rank
    # extended_user.rank = rank
    # extended_user.faculty = faculty
    extended_user.building = request.POST.get('building')
    extended_user.save()
    
    return JsonResponse({'success': True, 'message': 'Profile updated successfully'})

@login_required
@require_POST
def change_password(request):
    user = request.user
    current_password = request.POST.get('current_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')

    if not user.check_password(current_password):
        return JsonResponse({'success': False, 'message': 'Current password is incorrect'})

    if new_password1 != new_password2:
        return JsonResponse({'success': False, 'message': 'New passwords do not match'})

    user.set_password(new_password1)
    user.save()
    update_session_auth_hash(request, user)  # Important to keep the user logged in
    return JsonResponse({'success': True, 'message': 'Password changed successfully'})

@require_POST
@login_required(login_url='login')
def add_device(request):

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        serial_number = request.POST.get('serial_number')
        
        # Check for duplicate serial_number
        if Device.objects.filter(serial_number=serial_number).exists():
            error_message = 'Device with this serial number already exists.'
            return JsonResponse({'error': error_message})

        is_qrcode_applied = request.POST.get('is_qrcode_applied') == 'on'

        # Retrieve category and subcategory
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        category = Category.objects.get(id=category_id)
        subcategory = Subcategory.objects.get(id=subcategory_id)

        # Retrieve Owner as the user who adds it
        owner = request.user        

        # Retrieve building, floor, and room objects based on the selected IDs
        building_id = request.POST['building']
        floor_id = request.POST['floor']
        room_id = request.POST['room']

        building = Building.objects.get(id=building_id)
        inventory = Inventory.objects.get(id=building_id)
        floor = Floor.objects.get(id=floor_id)
        room = Room.objects.get(id=room_id)

        # Create Device object with provided data
        device = Device(
            name=name,
            description=description,
            serial_number=serial_number,
            category = category,
            subcategory = subcategory,
            owner = owner,
            is_qrcode_applied=is_qrcode_applied,
            building=building,
            inventory=inventory,
            floor=floor,
            room=room,
        )
        
        # Save the device
        device.save()


        # Redirect to the device_detail view for the newly created device
         # return redirect('device_detail', pk=device.pk)
        return JsonResponse({'success': 'Device added successfully','device_pk':device.pk})  # Redirect to the device list page

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def edit_device(request):
    
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
        device = get_object_or_404(Device, id=device_id)

        if not request.user == device.owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to edit this device.'})

        data = {
            'success': True,
            'device': {
                'id': device.id,
                'name': device.name,
                'description': device.description,
                'serial_number': device.serial_number,
                'category': device.category.id,
                'subcategory': device.subcategory.id,
                'building': device.building.id,
                'inventory': device.building.id,
                'floor': device.floor.id,
                'room': device.room.id,
            }
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        device_id = request.POST.get('device_id')
        device = get_object_or_404(Device, id=device_id)

        if not request.user == device.owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to edit this device.'})

        try:
            device.name = request.POST.get('name')
            device.description = request.POST.get('description')
            device.serial_number = request.POST.get('serial_number')
            device.owner = request.user

            category_id = request.POST.get('category')
            subcategory_id = request.POST.get('subcategory')
            building_id = request.POST.get('building')
            floor_id = request.POST.get('floor')
            room_id = request.POST.get('room')

            device.category = get_object_or_404(Category, id=category_id)
            device.subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            device.building = get_object_or_404(Building, id=building_id)
            device.inventory = get_object_or_404(Inventory, id=building_id)
            device.floor = get_object_or_404(Floor, id=floor_id)
            device.room = get_object_or_404(Room, id=room_id)

            device.updated_at = timezone.now()
            device.save()

            return JsonResponse({'success': True, 'message': 'Device updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
@require_POST
@login_required(login_url='login')
def delete_device(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')
        
        if not device_id:
            return JsonResponse({'success': False, 'message': 'Device ID not provided'}, status=400)
        
        device = get_object_or_404(Device, pk=device_id)

        if not request.user == device.owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to delete this device.'})

        device.delete()
        
        return JsonResponse({'success': True, 'message': 'Device deleted successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)




from django.views.generic import TemplateView
from .models import InventorizationList, Building

class InventoryManagementView(BaseContextMixin,LoginRequiredMixin, TemplateView):
    template_name = 'devices/inventory_management.html'

    def get_context_data(self, **kwargs):
        if is_inventory_manager(self.request.user) :
            inventory_id = self.kwargs.get('pk')
            inventory = Inventory.objects.get(id=inventory_id)
            inventory_device_list = Device.objects.filter(inventory__id=inventory_id,is_active=True)

            # Get statistics for inventorization lists
            total_lists = InventorizationList.objects.filter(inventory=inventory).count()
            completed_lists = InventorizationList.objects.filter(inventory=inventory, status='COMPLETED').count()
            
            # Get the latest inventory_change timestamp for the current inventory
            last_updated = InventoryChange.objects.filter(inventory_id=inventory_id).aggregate(Max('timestamp'))['timestamp__max']

            # Calculate total devices and total rooms
            total_devices = inventory_device_list.count()
            rooms = Room.objects.filter(building__id=inventory_id)
            total_rooms = rooms.count()

            context = self.get_base_context()
            context.update({
                'inventory': inventory,
                'inventorization_lists': InventorizationList.objects.filter(inventory=inventory).order_by('-start_date'),
                'total_lists': total_lists,
                'completed_lists': completed_lists,
                'devices': inventory_device_list,
                'total_devices': total_devices,
                'rooms': rooms,
                'total_rooms': total_rooms,
                'last_updated': last_updated,
                # 'recent_activities': RecentActivity.objects.all().order_by('-timestamp')[:10],  # Adjust as needed
                # 'history_entries': HistoryEntry.objects.all().order_by('-timestamp'),  # Adjust as needed
            })
            return context
        else:
            return redirect('homepage')

from django.views.generic import DetailView
from django.db.models import Count
from .models import InventorizationList, Device, Room, DeviceScan

class InventorizationListDetailView(BaseContextMixin,LoginRequiredMixin,DetailView):
    login_url='login'

    model = InventorizationList
    template_name = 'devices/inventorization_list_detail.html'
    context_object_name = 'inventory_list'

    def get_context_data(self, **kwargs):
        if is_inventory_manager(self.request.user) :
            context = super().get_context_data(**kwargs)
            context.update(self.get_base_context())

            # Get the inventory list object from the URL
            inventory_list = self.object
            inventory = inventory_list.inventory

            # Define Context Variables
            devices = {}
            scanned_devices_set = {}
            
            # Get the devices associated with the inventory
            if inventory_list.status == 'COMPLETED':
                # Load data from the JSON file
                with open(inventory_list.inventory_data_file.path, 'r') as f:
                    inventory_data = json.load(f)
                devices = inventory_data['devices']
                changes = inventory_data['changes']
                device_scans = inventory_data['device_scans']
                scanned_devices_set = set(scan['device_id'] for scan in device_scans)
                context['pdf_report_url'] = inventory_list.pdf_report.url if inventory_list.pdf_report else None
                context['excel_report_url'] = inventory_list.excel_report.url if inventory_list.excel_report else None

            else:
                # Check for message in session
                if 'qr_scan_message' in self.request.session:
                    context['qr_scan_message'] = self.request.session.pop('qr_scan_message')
                
                # Get devices and scanned devices based on the extracted device IDs
                devices = Device.objects.filter(inventory=inventory,is_active=True)
                
                scanned_devices = DeviceScan.objects.filter(inventory_list=inventory_list, device__in=devices)
                scanned_devices_set = set(scanned_devices.values_list('device_id', flat=True))

            # Update the context with the calculated values
            context['inventory'] = inventory
            context['inventory_list'] = inventory_list
            context['devices'] = devices
            context['scanned_devices'] = scanned_devices_set
            context['total_devices'] = inventory_list.total_devices
            context['total_scanned'] = inventory_list.total_scanned

            return context
        else:
            return redirect('homepage')
    
  

class DeviceDetailView(BaseContextMixin,LoginRequiredMixin, DetailView):
    login_url='login'

    model = Device
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
        try:
            iot_device = IoTDevice.objects.filter(device=self.object).first()
            context['iot_device'] = iot_device
            context['user_device'] = self.request.user == self.object.owner
            context['timestamp'] = now().timestamp()
        except:
            pass
        
        return context

    def get(self, request, *args, **kwargs):
        # Call the parent class's get() method to set self.object
        response = super().get(request, *args, **kwargs)
        
        device = self.object
        user = request.user

        # Check if this is a QR code scan
        is_qr_scan = request.GET.get('source') == 'qr_scan'

        # Only process as inventory scan if it's a QR code scan and user is an inventory manager
        if is_qr_scan and user.groups.filter(name='Inventory-Managers').exists():
            # Check for active inventorization list created by this user
            active_inventory = InventorizationList.objects.filter(
                creator=user,
                status='ACTIVE',
                building=device.building
            ).first()

            paused_inventory = InventorizationList.objects.filter(
                creator=user,
                status='PAUSED',
                building=device.building
            ).first()

            if active_inventory:
                # Check if the device's room is part of the inventory
                if device.inventory == active_inventory.inventory:
                    # Record the scan
                    active_inventory.scan_device(device.id)

                    request.session['qr_scan_message'] = {
                        'type': 'success',
                        'text': f"Device {device.name} scanned successfully for inventory {active_inventory.id}."
                    }
                    return redirect('inventory_detail', pk=active_inventory.id)
                else:
                    request.session['qr_scan_message'] = {
                        'type': 'warning',
                        'text': f"This device is not part of the active inventory {active_inventory.id}."
                    }
            elif paused_inventory:
                request.session['qr_scan_message'] = {
                        'type': 'warning',
                        'text': f"This inventory {paused_inventory.id} is currently paused. Please resume the inventory to scan devices."
                }
                return redirect('inventory_detail', pk=paused_inventory.id)

        context = self.get_context_data(object=device,user=user)
        return response

class DownloadQRCodeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, device_id):

        try:
            device = Device.objects.get(pk=device_id)
            # Construct the complete URL for the QR code image
            qr_code_url = request.build_absolute_uri(device.qrcode_url)
            
            # Fetch the QR code image using requests
            response = requests.get(qr_code_url)
            
            response.raise_for_status()  # Check for request success
            
            qr_code_image = response.content
            
            # Prepare response
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={device.id}_{device.serial_number}_qrcode.png'
            response.write(qr_code_image)

            return response
    
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)
        except requests.exceptions.HTTPError:
            return JsonResponse({"error": "Failed to fetch QR code image"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


