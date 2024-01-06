# devices/tables.py
import django_tables2 as tables
from .models import Device

class DeviceTable(tables.Table):
    
    name = tables.Column(orderable=True)
    description = tables.Column(orderable=True)

    class Meta:
        model = Device
        template_name = 'django_tables2/bootstrap5.html'  # Use the Bootstrap 5 theme
        fields = ('name', 'description')  # Specify the fields you want to include in the table
