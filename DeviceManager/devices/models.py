# devices/models.py
# devices/models.py
import json
from django.db import models
from django.urls import reverse
from django.contrib.sites.models import Site
import qrcode
import os
from django.conf import settings
import datetime
from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ExtendedUser(models.Model):

    RANK_CHOICES = [
        ('PROF', 'Profesor (Professor)'),
        ('CONF', 'Conferentiar (Associate Professor)'),
        ('LECTOR', 'Șef lucrări (Lecturer)'),
        ('ASIST', 'Asistent universitar (Assistant)'),
        ('ENG', 'Engineer'),
        ('None' , 'None'),
    ]

    ACRONYM_RANK_CHOICES = [
        ('PROF', 'Prof.dr.ing.'),
        ('CONF', 'Conf.dr.ing.'),
        ('LECTOR', 'Șef lucrări dr.ing.'),
        ('ASIST', 'Asist.dr.ing.'),
        ('ENG', 'Eng.'),
        ('None' , 'None'),
    ]
    

    ADMIN_RANK_CHOICES = [
        ('RECTOR', 'Rector'),
        ('PRORECTOR', 'Vice-rector'),
        ('DECAN', 'Decan (Dean)'),
        ('PRODECAN', 'Prodecan (Vice-dean)'),
        ('DIR_DEPT', 'Director de departament (Head of department)'),
        ('SEF_DISC', 'Șef de disciplină (Head of a subject)'),
        ('None' , 'None'),
    ]
    FACULTY_CHOICES = [
        ('AC', 'Faculty of Automatic Control & Computer Engineering'),
        ('EE', 'Faculty of Electrical Engineering'),
        ('ETTI', 'Faculty of Electronics, Telecommunications & Information Technology'),
        ('CEBS', 'Faculty of Civil Engineering & Building Services'),
        ('CEEP', 'Faculty of „Cristofor Simionescu” Chemical Engineering & Environmental Protection'),
        ('MMIM', 'Faculty of Machine Manufacturing & Industrial Management'),
        ('ARCH', 'Faculty of „G. M. Cantacuzino” Architecture'),
        ('HGEE', 'Faculty of Hydrotechnics, Geodesy & Environmental Engineering'),
        ('ME', 'Faculty of Mechanical Engineering'),
        ('SIM', 'Faculty of Material Science & Engineering'),
        ('IDBM', 'Faculty of Industrial Design and Business Management'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_user')
    age = models.PositiveIntegerField(null=True, blank=True)
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, blank=True)
    acronym_rank = models.CharField(max_length=20, choices=ACRONYM_RANK_CHOICES, blank=True)
    admin_rank = models.CharField(max_length=20, choices=ADMIN_RANK_CHOICES, blank=True)
    faculty = models.CharField(max_length=4, choices=FACULTY_CHOICES, blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Ensure acronym_rank matches rank
        if self.rank:
            self.acronym_rank = self.rank
        super().save(*args, **kwargs)
    
    def get_full_name_with_title(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        if not full_name:
            full_name = self.user.username
        
        titles = []

        if self.admin_rank and self.admin_rank != 'None':
            titles.append(dict(self.ADMIN_RANK_CHOICES)[self.admin_rank].split('(')[0].strip())
        if self.rank and self.rank != 'None':
            titles.append(dict(self.ACRONYM_RANK_CHOICES)[self.rank].split('(')[0].strip())
        
        if titles:
            return f"{' '.join(titles)} {full_name}".strip()
        else:
            return full_name

@receiver(post_save, sender=User)
def create_or_update_extended_user(sender, instance, created, **kwargs):
    ExtendedUser.objects.get_or_create(user=instance)



class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    acronym = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f'{self.pk } - {self.name}'

    class Meta:
        ordering = ['id']

class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)

    
    def __str__(self):
        return f'{self.pk} - {self.building.acronym} - Floor {self.name}'

    class Meta:
        ordering = ['id']

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)  # Assuming a room number can be up to 5 characters

    def __str__(self):
        return f'{self.pk} - {self.building.acronym} - Floor {self.floor.name} - {self.name}'
    
    class Meta:
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk} - {self.name}'

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.category} - {self.name}'

class Inventory(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.building.name}'



class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=25,unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_devices')

    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)  # New field
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  # Choices: laptop, pc, router, server
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)

    # QR Code
    is_qrcode_applied = models.BooleanField(default=False)
    qrcode_path = models.CharField(max_length=255, blank=True, null=True)
    qrcode_target_url = models.URLField(max_length=255, blank=True, null=True)

    # Location Related
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    is_active = models.BooleanField(default=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)
    deactivation_change = models.ForeignKey('InventoryChange', null=True, blank=True, on_delete=models.SET_NULL, related_name='deactivated_device')


    def __str__(self):
        return f"{self.id} - {self.name} - {self.serial_number}"
    
    @property
    def qrcode_url(self):
        if self.qrcode_path:
            return settings.MEDIA_URL + self.qrcode_path
        return None
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.generate_qr_code()
            InventoryChange.objects.create(
                inventory=self.inventory,
                device=self,
                change_type='ADD',
                user=self.owner
            )
        else:
            InventoryChange.objects.create(
                inventory=self.inventory,
                device=self,
                change_type='EDIT',
                user=self.owner
            )
        


        # Update associated InventorizationList
        InventorizationList.objects.filter(
            inventory=self.inventory, 
            status__in=['ACTIVE', 'PAUSED']
        ).update(total_devices=models.F('total_devices') + (1 if is_new else 0))

    def soft_delete(self, inventory_change):
        Device.objects.filter(pk=self.pk).update(
            is_active=False,
            deactivation_date=timezone.now(),
            deactivation_change=inventory_change
        )

    def delete(self, *args, **kwargs):
        inventory = self.inventory
        inventory_change = InventoryChange.objects.create(
            inventory=inventory,
            device=self,
            change_type='REMOVE',
            user=self.owner
        )
        self.soft_delete(inventory_change)

        # Update associated InventorizationList
        InventorizationList.objects.filter(
            inventory=inventory, 
            status__in=['ACTIVE', 'PAUSED']
        ).update(total_devices=models.F('total_devices') - 1,total_scanned=models.F('total_scanned') - 1)
        
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        device_url = reverse('device_detail', args=[str(self.pk)])
        current_site = Site.objects.get_current()

        self.qrcode_target_url = f"http://{current_site.domain}{device_url}?source=qr_scan"

        qr.add_data(self.qrcode_target_url)
        qr.make(fit=True)

        img_path = f'qrcodes/{self.pk}.png'
        full_path = os.path.join(settings.MEDIA_ROOT, img_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(full_path)

        self.qrcode_path = img_path
        self.is_qrcode_applied = True

        # Update only the QR code related fields to avoid triggering the save method again
        Device.objects.filter(pk=self.pk).update(
            qrcode_path=self.qrcode_path,
            qrcode_target_url=self.qrcode_target_url,
            is_qrcode_applied=self.is_qrcode_applied
        )

    def regenerate_qr_code(self):
        if self.qrcode_path:
            old_path = os.path.join(settings.MEDIA_ROOT, self.qrcode_path)
            if os.path.exists(old_path):
                os.remove(old_path)

        self.qrcode_path = None
        self.qrcode_target_url = None
        self.is_qrcode_applied = False
        self.save(update_fields=['qrcode_path', 'qrcode_target_url', 'is_qrcode_applied'])

        self.generate_qr_code()
    
    class Meta:
        ordering = ['id']
    
class InventoryChange(models.Model):
    CHANGE_TYPES = (
        ('ADD', 'Add'),
        ('REMOVE', 'Remove'),
        ('EDIT', 'Edit'),
    )

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.id} - {self.get_change_type_display()} - {self.device} in {self.inventory.name} by {self.user} on {self.timestamp}"

class InventorizationList(models.Model):
    SCOPE_CHOICES = [
        ('ENTIRE', 'Entire Building'),
        ('PARTIAL', 'Selected Rooms'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
        ('UNKNOWN', 'Unknown'),
    ]

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE,blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_inventorizations')
    start_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True)
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    total_devices = models.IntegerField(default=0)
    total_scanned = models.IntegerField(default=0)

    inventory_data_file = models.FileField(upload_to='inventorization_data/', null=True, blank=True)

    def __str__(self):
        return f"Inventorization {self.id} by {self.creator.username}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.initialize_inventory_data()

    def initialize_inventory_data(self):
        self.total_devices = Device.objects.filter(inventory=self.inventory,is_active=True).count()
        self.total_scanned = 0
        self.save(update_fields=['total_devices', 'total_scanned'])

    def update_total_devices(self):
        if self.status in ['ACTIVE', 'PAUSED']:
            self.total_devices = Device.objects.filter(inventory=self.inventory).count()
            self.save(update_fields=['total_devices'])

    def scan_device(self, device_id):
        device = Device.objects.get(id=device_id)
        scan, created = DeviceScan.objects.get_or_create(inventory_list=self, device=device)
        print(device,scan,created)
        if created:
            self.total_scanned += 1
            self.save(update_fields=['total_scanned'])


    def end_inventory_list(self):
        self.status = 'COMPLETED'
        self.end_date = timezone.now()
        self.save()
        self.complete_inventorization()

    def complete_inventorization(self):
        self.status = 'COMPLETED'
        self.end_date = timezone.now()

        devices = Device.objects.filter(inventory=self.inventory,is_active=True).select_related(
            'category', 'subcategory', 'owner', 'room__building', 'room__floor'
        )        
        device_scans = DeviceScan.objects.filter(inventory_list=self, device__is_active=True)

        # Get all the changes since the last completed inventorization
        last_completed = InventorizationList.objects.filter(
            inventory=self.inventory,
            status='COMPLETED',
            end_date__lt=self.start_date
        ).order_by('-end_date').first()

        start_date = last_completed.end_date if last_completed else self.inventory.created_at

        changes = [self.change_to_dict(change) for change in InventoryChange.objects.filter(
            inventory=self.inventory,
            timestamp__gte=start_date,
            timestamp__lte=self.end_date
        ).select_related('device', 'user')]
        
        inventory_data = {
            'inventorization_id': self.id,
            'creator': self.creator.username,
            'inventory': self.inventory.name,
            'building': self.building.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'total_devices': self.total_devices,
            'total_scanned': self.total_scanned,
            'devices': [self.device_to_dict(device) for device in devices],
            'device_scans': [self.device_scan_to_dict(scan) for scan in device_scans],
            'changes': changes,
        }

        file_name = f'inventorization_{self.id}.json'
        file_path = os.path.join(settings.MEDIA_ROOT, 'inventorization_data', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(inventory_data, f, indent=4)

        self.inventory_data_file.name = f'inventorization_data/{file_name}'
        self.save()

    @staticmethod
    def device_to_dict(device):
        return {
            'id': device.id,
            'name': device.name,
            'serial_number': device.serial_number,
            'category': {
                'id': device.category.id,
                'name': device.category.name
            },
            'subcategory': {
                'id': device.subcategory.id,
                'name': device.subcategory.name
            },
            'owner': device.owner.username if device.owner else None,
            'building': {
                'id': device.building.id,
                'name': device.building.name,
                'acronym': device.building.acronym
            },
            'floor': {
                'id': device.floor.id,
                'name': device.floor.name
            },
            'room': {
                'id': device.room.id,
                'name': device.room.name
            }
        }

    @staticmethod
    def change_to_dict(change):
        return {
            'id': change.id,
            'device_id': change.device.id,
            'change_type': change.change_type,
            'timestamp': change.timestamp.isoformat(),
            'user': change.user.username if change.user else None,
        }

    @staticmethod
    def device_scan_to_dict(scan):
        return {
            'id': scan.id,
            'device_id': scan.device.id,
            'scanned_at': scan.scanned_at.isoformat(),
            'user': scan.user.username if scan.user else None,
        }
    
    class Meta:
        ordering = ['-start_date']


class DeviceScan(models.Model):
    inventory_list = models.ForeignKey(InventorizationList, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('inventory_list', 'device')



class IoTDevice(Device):
    ip_address = models.GenericIPAddressField()
    last_checked = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"IoT Device: {self.name}"

class IoTDeviceEndpoint(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, related_name='endpoints')
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10, default='GET')

    def __str__(self):
        return f"{self.device.name} - {self.name}"

    class Meta:
        unique_together = ['device', 'name']

class IoTDeviceResponse(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, related_name='responses')
    endpoint = models.ForeignKey(IoTDeviceEndpoint, on_delete=models.SET_NULL, null=True, related_name='responses')
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    response_time = models.FloatField()  # in seconds
    response_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.device.name} - {self.endpoint.name if self.endpoint else 'Unknown'} response at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

