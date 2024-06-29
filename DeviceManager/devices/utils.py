# devices/utils.py

import io
from django.template.loader import get_template
from django.db.models import Count, Q
from xhtml2pdf import pisa
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from .models import Room, Device, DeviceScan

def generate_inventory_pdf_report(inventory):
    # Get the template
    template = get_template('devices/inventory_report_pdf.html')
    
    # Get rooms associated with this inventory
    rooms = Room.objects.filter(id__in=inventory.room_ids)
    
    # Calculate totals
    total_devices = Device.objects.filter(room__in=rooms).count()
    total_scanned = DeviceScan.objects.filter(inventory=inventory).count()
    
    # Prepare the context
    context = {
        'inventory': inventory,
        'rooms_data': [],
        'total_devices': total_devices,
        'total_scanned': total_scanned
    }
    
    for room in rooms:
        devices = Device.objects.filter(room=room)
        scanned_devices = devices.filter(devicescan__inventory=inventory)
        context['rooms_data'].append({
            'room': room,
            'devices': devices,
            'scanned_devices': scanned_devices
        })

    # Render the template
    html = template.render(context)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # If error creating PDF, return None
    if pisa_status.err:
        return None
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return buffer

# devices/utils.py

from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.utils import get_column_letter

# devices/utils.py

from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.utils import get_column_letter

def generate_inventory_excel_report(inventory):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Inventory Report - {inventory.id}"

    # Styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="34495E", end_color="34495E", fill_type="solid")
    centered = Alignment(horizontal='center', vertical='center')
    wrapped = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    red_fill = PatternFill(start_color="E74C3C", end_color="E74C3C", fill_type="solid")
    green_fill = PatternFill(start_color="2ECC71", end_color="2ECC71", fill_type="solid")
    orange_fill = PatternFill(start_color="F39C12", end_color="F39C12", fill_type="solid")
    gray_fill = PatternFill(start_color="95A5A6", end_color="95A5A6", fill_type="solid")

    # General Information
    ws.append(["Inventory Report"])
    ws.append(["ID", inventory.id])
    ws.append(["Creator", inventory.creator.username])
    ws.append(["Building", inventory.building.name])
    ws.append(["Start Date", inventory.start_date.strftime("%Y-%m-%d %H:%M")])
    ws.append(["End Date", inventory.end_date.strftime("%Y-%m-d %H:%M") if inventory.end_date else "Not ended"])
    ws.append(["Status", inventory.get_status_display()])
    ws.append(["Scope", inventory.get_scope_display()])

    rooms = Room.objects.filter(id__in=inventory.room_ids)
    total_devices = Device.objects.filter(room__in=rooms).count()
    total_scanned = DeviceScan.objects.filter(inventory=inventory).count()
    
    ws.append(["Total Devices", total_devices])
    ws.append(["Scanned Devices", f"{total_scanned} / {total_devices}"])
    
    progress = (total_scanned / total_devices * 100) if total_devices > 0 else 0
    ws.append(["Progress", f"{progress:.2f}%"])

    # Color the status cell
    status_cell = ws.cell(row=7, column=2)
    if inventory.status == 'ACTIVE':
        status_cell.font = Font(color="2ECC71", bold=True)
    elif inventory.status == 'COMPLETED':
        status_cell.fill = green_fill
        status_cell.font = Font(color="FFFFFF", bold=True)
    elif inventory.status == 'CANCELED':
        status_cell.fill = red_fill
        status_cell.font = Font(color="FFFFFF", bold=True)
    elif inventory.status == 'PAUSED':
        status_cell.fill = orange_fill
        status_cell.font = Font(color="FFFFFF", bold=True)

    # Color the progress cell
    progress_cell = ws.cell(row=11, column=2)
    if progress == 0:
        progress_cell.fill = red_fill
    elif progress == 100:
        progress_cell.fill = green_fill
    else:
        progress_cell.fill = orange_fill
    progress_cell.font = Font(color="FFFFFF", bold=True)

    ws.append([])  # Empty row for spacing

    # Rooms and Devices
    headers = ["ID", "Name", "Serial Number", "Category", "Subcategory", "Building", "Floor", "Room", "Status", "Last Updated"]
    
    for room in rooms:
        ws.append([f"Room: {room.name}"])
        ws.append(headers)
        for cell in ws[ws.max_row]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = centered
            cell.border = border

        devices = Device.objects.filter(room=room)
        scanned_devices = devices.filter(devicescan__inventory=inventory)

        room_start_row = ws.max_row + 1
        for device in devices:
            row = [
                device.id,
                device.name,
                device.serial_number,
                device.category.name,
                device.subcategory.name,
                device.building.name,
                device.floor.name,
                device.room.name,
                "Scanned" if device in scanned_devices else "Not Scanned",
                device.updated_at.strftime("%Y-%m-d %H:%M")
            ]
            ws.append(row)
            for cell in ws[ws.max_row]:
                cell.border = border
                cell.alignment = wrapped
            
            # Color the status cell
            status_cell = ws.cell(row=ws.max_row, column=9)
            if device in scanned_devices:
                status_cell.fill = green_fill
            else:
                status_cell.fill = red_fill

        room_end_row = ws.max_row
        
        # Color the room header based on scan status
        room_header = ws.cell(row=room_start_row - 2, column=1)
        if devices.count() == 0:
            room_header.fill = gray_fill
        elif scanned_devices.count() == 0:
            room_header.fill = red_fill
        elif scanned_devices.count() == devices.count():
            room_header.fill = green_fill
        else:
            room_header.fill = orange_fill

        ws.append([])  # Empty row for spacing

    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width

    # Make the building column wider
    ws.column_dimensions['F'].width = 30

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
