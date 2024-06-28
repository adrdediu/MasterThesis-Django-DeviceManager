# devices/views.py
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.views.generic import DetailView, TemplateView
from .models import Device,Floor,Room,Building,Subcategory,Category
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
        subcategories = Subcategory.objects.filter(category_id=category_id)
        data =[{'id':subcategory.id,'name':subcategory.name} for subcategory in subcategories]
        return JsonResponse(data,safe=False)
    
class GetFloorsView(View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        building_id = self.request.GET.get('building_id')
        floors = Floor.objects.filter(building_id=building_id)
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
        devices = Device.objects.all()

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

@login_required(login_url='login')
def add_device(request):

    buildings = Building.objects.all()
    floors = Floor.objects.all()
    rooms = Room.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    context = {
        'buildings': buildings,
        'floors': floors,
        'rooms': rooms,
        'categories': categories,
        'subcategories': subcategories,
    }

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

    return render(request, 'devices/device_list.html', context)



class ActionsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'

    template_name = 'devices/actions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        # Add any other context data you need for the actions page
        return context

    

class DeviceDetailView(LoginRequiredMixin,DetailView):
    login_url = 'login'

    model = Device
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'

class DownloadQRCodeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, device_id):
        # Fetch the device
        device = get_object_or_404(Device, pk=device_id)

        # Construct the complete URL for the QR code image
        qr_code_url = request.build_absolute_uri(device.qrcode_url)

        # Fetch the QR code image using requests
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