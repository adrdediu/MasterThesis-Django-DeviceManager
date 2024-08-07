from datetime import timezone
from django.views.generic import View
from django.http import StreamingHttpResponse
from django.utils.timezone import now
import json
import time
from .models import IoTDeviceResponse,IoTDevice



class SSEDeviceUpdateView(View):
    def get(self, request, device_id, *args, **kwargs):
        return StreamingHttpResponse(self.event_stream(device_id), content_type='text/event-stream')

    def event_stream(self, device_id):
        iotDevice = IoTDevice.objects.get(device_id=device_id)
        last_id = 0
        while True:
            latest_response = IoTDeviceResponse.objects.filter(device=iotDevice).order_by('-last_checked').first()
            
            if latest_response and latest_response.id > last_id:
                is_online = latest_response.last_status_code == 200
                
                last_successful_response = IoTDeviceResponse.objects.filter(
                    device=iotDevice,
                    last_status_code=200
                ).order_by('-last_checked').first()
                
                time_elapsed = None
                if last_successful_response:
                    time_elapsed = (now() - last_successful_response.last_checked).total_seconds()
                print(f"Time elapsed: {time_elapsed}")
                data = {
                    'id': latest_response.id,
                    'status_code': latest_response.last_status_code,
                    'timestamp': latest_response.last_checked.isoformat(),
                    'is_online': is_online,
                    'time_elapsed': time_elapsed
                }
                yield f"data: {json.dumps(data)}\n\n"
                
            yield f": keepalive {now()}\n\n"
            time.sleep(1)

