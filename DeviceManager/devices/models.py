# devices/models.py
# devices/models.py
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

class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=50,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  # Choices: laptop, pc, router, server
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)

    # QR Code
    is_qrcode_applied = models.BooleanField(default=False)
    qrcode_url = models.CharField(max_length=255,blank=True, null=True)

    # Location Related
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.qrcode_url:
            self.generate_qr_code()

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Generate the device URL with the qr_scan parameter
        device_url = reverse('device_detail', args=[str(self.pk)])
        current_site = Site.objects.get_current()

        complete_url = f"http://{current_site.domain}{device_url}?source=qr_scan"

        qr.add_data(complete_url)
        qr.make(fit=True)

        img_path = os.path.join(settings.MEDIA_ROOT, f'qrcodes/{self.pk}.png')
        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(img_path)

        self.qrcode_url = settings.MEDIA_URL + f'qrcodes/{self.pk}.png'
        self.is_qrcode_applied = True
        self.save(update_fields=['qrcode_url', 'is_qrcode_applied'])

    def regenerate_qr_code(self):
        # Delete the old QR code file if it exists
        if self.qrcode_url:
            old_path = os.path.join(settings.MEDIA_ROOT, self.qrcode_url.lstrip('/'))
            if os.path.exists(old_path):
                os.remove(old_path)

        # Reset QR code fields
        self.qrcode_url = None
        self.is_qrcode_applied = False
        self.save(update_fields=['qrcode_url', 'is_qrcode_applied'])

        # Generate new QR code
        self.generate_qr_code()

    class Meta:
        ordering = ['id']
    

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

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_inventorizations')
    start_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True)
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES)
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    room_ids = JSONField(default=list)  # This will store the list of room IDs
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"Inventorization {self.id} by {self.creator.username}"

    class Meta:
        ordering = ['-start_date']

class InventorizationRoom(models.Model):
    inventorization = models.ForeignKey(InventorizationList, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room.name} in Inventorization {self.inventorization.id}"

class InventorizationDevice(models.Model):
    inventorization_room = models.ForeignKey(InventorizationRoom, on_delete=models.CASCADE, related_name='devices')
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    is_scanned = models.BooleanField(default=False)
    scan_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Device {self.device.name} in Room {self.inventorization_room.room.name}"

class DeviceScan(models.Model):
    inventory = models.ForeignKey(InventorizationList, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('inventory', 'device')


