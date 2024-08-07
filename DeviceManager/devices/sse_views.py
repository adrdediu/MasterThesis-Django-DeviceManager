from datetime import timezone
from django.views.generic import View
from django.http import StreamingHttpResponse
from django.utils.timezone import now
import json
import time
from .models import IoTDeviceResponse,IoTDevice

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    else:
        days = seconds / 86400
        return f"{days:.2f} days"


class SSEDeviceUpdateView(View):
    def get(self, request, device_id, *args, **kwargs):
        return StreamingHttpResponse(self.event_stream(device_id), content_type='text/event-stream')

    def event_stream(self, device_id):
        iotDevice = IoTDevice.objects.get(device_id=device_id)
        last_id = 0
        while True:
            new_responses = IoTDeviceResponse.objects.filter(
                device=iotDevice, 
                id__gt=last_id
            ).order_by('id')
            if new_responses.exists():
                for response in new_responses:
                    last_successful_response = IoTDeviceResponse.objects.filter(
                        device=iotDevice,
                        status_code=200,
                        id__lt=response.id
                    ).order_by('-id').first()
                    print(last_successful_response)
                    time_elapsed = (response.timestamp - last_successful_response.timestamp).total_seconds() if last_successful_response else None
                    print(time_elapsed) 
                    data = {
                        'id': response.id,
                        'status_code': response.status_code,
                        'timestamp': response.timestamp.isoformat(),
                        'response_data': response.response_data,
                        'time_elapsed': time_elapsed
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                last_id = new_responses.last().id
            yield f": keepalive {now()}\n\n"
            time.sleep(0.25)

