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
        return self.name 

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

            # Generate QR code with the device detail URL
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            device_url = reverse('device_detail', args=[str(self.pk)])

            # Ensure to use the correct domain
            current_site = Site.objects.get_current()
            complete_url = f"http://{current_site.domain}{device_url}"

            qr.add_data(complete_url)
            qr.make(fit=True)

            # Specify the full path to save the QR code image
            img_path = os.path.join(settings.MEDIA_ROOT, f'qrcodes/{self.pk}.png')

            # Ensure the directory exists before saving the file
            os.makedirs(os.path.dirname(img_path), exist_ok=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(img_path)

            # Save the complete QR code URL to the model field
            self.qrcode_url = settings.MEDIA_URL + f'qrcodes/{self.pk}.png'

            self.updated_at = timezone.now()
            print(self.updated_at,timezone.now())
            super().save(update_fields=['qrcode_url'])
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('device_detail', args=[str(self.pk)])