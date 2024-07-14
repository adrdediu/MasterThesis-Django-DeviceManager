# devices/views.py
import requests
import json
import os
import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, FileResponse,HttpResponseBadRequest,HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm
from django.views.generic import DetailView, TemplateView
from .models import Device,Floor,Room,Building,Subcategory,Category
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .utils import generate_inventory_excel_report,generate_inventory_pdf_report
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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
        buildings = Building.objects.all()
        floors = Floor.objects.all()
        rooms = Room.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        return {
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
        devices = Device.objects.all().order_by('-id')

        selected_category = selected_subcategory = selected_building = selected_floor = selected_room = ""

        if category:
            selected_category_object = get_object_or_404(Category, name=category)
            selected_category = selected_category_object.name
            if subcategory:
                selected_subcategory = get_object_or_404(Subcategory, name=subcategory, category=selected_category_object.id).name

        if building:
            selected_building_object = get_object_or_404(Building, name=building)
            selected_building = selected_building_object.name
            if floor:
                selected_floor_object = get_object_or_404(Floor, building=selected_building_object.id, name=floor).name
                selected_floor = selected_floor_object.name
                if room:
                    selected_room = get_object_or_404(Room, building=selected_building_object.id, floor=selected_floor_object.id, name=room).name

        context = self.get_base_context()
        context.update({
            'devices': devices,
            'selected_category': selected_category,
            'selected_subcategory': selected_subcategory,
            'selected_building': selected_building,
            'selected_floor': selected_floor,
            'selected_room': selected_room,
        })

        return render(request, 'devices/device_list.html', context)


@login_required
@require_POST
def update_profile(request):
    user = request.user
    password = request.POST.get('password')
    print(password)
    print(user.check_password(password))
    if not user.check_password(password):
        return JsonResponse({'success': False, 'message': 'Incorrect password'})
    
    # Validate email
    email = request.POST.get('email')
    print(email)
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
    rank = request.POST.get('rank')
    faculty = request.POST.get('faculty')
    if rank not in dict(user.extended_user.RANK_CHOICES):
        return JsonResponse({'success': False, 'message': 'Invalid rank selected'})
    if faculty not in dict(user.extended_user.FACULTY_CHOICES):
        return JsonResponse({'success': False, 'message': 'Invalid faculty selected'})

    # Update user information
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    
    # Update extended user information
    extended_user = user.extended_user
    extended_user.rank = rank
    extended_user.faculty = faculty
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
                'floor': device.floor.id,
                'room': device.room.id,
            }
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        device_id = request.POST.get('device_id')
        device = get_object_or_404(Device, id=device_id)
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
            device.floor = get_object_or_404(Floor, id=floor_id)
            device.room = get_object_or_404(Room, id=room_id)

            device.updated_at = datetime.datetime.now()

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
        context = self.get_base_context(**kwargs)
        context.update({
            'inventorization_lists': InventorizationList.objects.all().order_by('-start_date'),
            #'recent_activities': RecentActivity.objects.all().order_by('-timestamp')[:10],  # Adjust as needed
            #'history_entries': HistoryEntry.objects.all().order_by('-timestamp'),  # Adjust as needed
        })
        return context

from django.views.generic import DetailView
from django.db.models import Count
from .models import InventorizationList, Device, Room, DeviceScan

class InventorizationListDetailView(BaseContextMixin,LoginRequiredMixin,DetailView):
    login_url='login'

    model = InventorizationList
    template_name = 'devices/inventorization_list_detail.html'
    context_object_name = 'inventory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
        inventory = self.object

        # Check for message in session
        if 'qr_scan_message' in self.request.session:
            context['qr_scan_message'] = self.request.session.pop('qr_scan_message')
        
        # Use room_data from the inventory object
        room_data = inventory.room_data

        # Extract device IDs from room_data
        device_ids = []
        for room_info in room_data.values():
            device_ids.extend(device['id'] for device in room_info['devices'])

        # Get devices and scanned devices based on the extracted device IDs
        devices = Device.objects.filter(id__in=device_ids).select_related(
            'category', 'subcategory', 'room', 'room__floor', 'room__building'
        )    
        scanned_devices = DeviceScan.objects.filter(inventory=inventory, device__in=device_ids)
        scanned_devices_set = set(scanned_devices.values_list('device_id', flat=True))

        context['devices'] = devices
        context['scanned_devices'] = scanned_devices_set
        context['total_devices'] = inventory.total_devices
        context['total_scanned'] = inventory.total_scanned

        return context
    
  

class DeviceDetailView(BaseContextMixin,LoginRequiredMixin, DetailView):
    login_url='login'

    model = Device
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
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
                if device.room.id in active_inventory.room_ids:
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

        context = self.get_context_data(object=device)
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
            response = requests.get(qr_code_url)
            response.raise_for_status()  # Check for request success
            qr_code_image = Image.open(BytesIO(response.content))

            # Resize the image to a smaller size
            new_size = (100, 100)  # Adjust the size as needed
            qr_code_image = qr_code_image.resize(new_size)

            # Get a font for drawing text (adjust the font size and style as needed)
            font = ImageFont.truetype("arial.ttf", size=12)

            # Create a new image with a white background
            image = Image.new('RGB', (new_size[0], new_size[1] + 30), 'white')


            # Create a drawing object
            draw = ImageDraw.Draw(image)
            # Draw ID above QR code 
            id_text = f"ID: {device.id}"
            draw.text((10, 10), id_text, font=font, fill=(0, 0, 0))

            # Draw serial number below ID, above QR code
            #serial_text = f"Serial: {device.serial_number}" 
            #draw.text((10, 50), serial_text, font=font, fill=(0, 0, 0)) 

            # Draw name below QR code
            #name_text = f"{device.name}"
            #draw.text((10, 10), name_text, font=font, fill=(0, 0, 0))

            # Draw QR code image
            image.paste(qr_code_image, (0, 30))


            # Save the modified image to an in-memory buffer
            modified_image_buffer = BytesIO()
            image.save(modified_image_buffer, format='PNG')
            modified_image_buffer.seek(0)

            # Prepare response
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={device.id}_{device.serial_number}_qrcode.png'
            response.write(modified_image_buffer.read())

            return response
    
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)
        except requests.exceptions.HTTPError:
            return JsonResponse({"error": "Failed to fetch QR code image"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_POST
def generate_inventory_report_view(request, inventory_id):
    inventory = get_object_or_404(InventorizationList, id=inventory_id)
    
    # Check permissions here if needed
    if request.user != inventory.creator and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to generate this report.")
    
    report_type = request.POST.get('report_type', 'pdf')
    
    if report_type == 'pdf':
        report_file = generate_inventory_pdf_report(inventory)
        if report_file is None:
            return HttpResponseServerError("Failed to generate PDF report")
        filename = f'inventory_report_{inventory_id}.pdf'
        content_type = 'application/pdf'
    elif report_type == 'excel':
        report_file = generate_inventory_excel_report(inventory)
        filename = f'inventory_report_{inventory_id}.xlsx'
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        return HttpResponseBadRequest("Invalid report type")
    
    # Return the file
    return FileResponse(report_file, as_attachment=True, filename=filename, content_type=content_type)


#Include only Next JS Related Imports
from django.utils.safestring import mark_safe
from .serializers import DeviceSerializer, CategorySerializer, UserSerializer


class NextJSView(BaseContextMixin,TemplateView):
    template_name = 'devices/nextjs_template.html'

    def get_context_data(self, **kwargs):
        context = self.get_base_context(**kwargs)
        context['next_js_url'] = 'static/js/next/index.html'
        return context    
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'devices/nextjs_template.html'
    login_url = '/login/'  # Specify the login URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        devices = Device.objects.all()
        categories = Category.objects.all()
        
        next_js_context = {
            'user': UserSerializer(self.request.user).data,
            'devices': DeviceSerializer(devices, many=True).data,
            'categories': CategorySerializer(categories, many=True).data,
        }
        
        # Convert to JSON and mark as safe for rendering in template
        context['next_js_context_json'] = mark_safe(json.dumps(next_js_context))

        context['next_js_url'] = f'static/js/next/dashboard.html'
        return context
