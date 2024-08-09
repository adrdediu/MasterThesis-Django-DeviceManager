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
        last_id = 0
        while True:
            iotDevice = IoTDevice.objects.get(device_id=device_id)
            latest_response = IoTDeviceResponse.objects.filter(device=iotDevice).order_by('-last_checked').first()
            
            if latest_response and latest_response.id > last_id:
                last_successful_response = IoTDeviceResponse.objects.filter(
                    device=iotDevice,
                    last_status_code=200
                ).order_by('-last_checked').first()
                last_unauthorised_response = IoTDeviceResponse.objects.filter(
                    device=iotDevice,
                    last_status_code=401
                ).order_by('-last_checked').first()

                time_elapsed = None
                is_online = 0
                latest_data = None

                if last_successful_response == latest_response:
                    time_elapsed = (now() - last_successful_response.last_checked).total_seconds()
                    is_online = 1 if time_elapsed < 30 else 0

                else:
                    if last_unauthorised_response == latest_response:
                        is_online = 2
                        time_elapsed = (now() - last_unauthorised_response.last_checked).total_seconds()
                    elif last_successful_response and last_unauthorised_response:
                        time_elapsed = (now() - max(last_successful_response.last_checked, last_unauthorised_response.last_checked)).total_seconds()
                    elif last_successful_response:
                        time_elapsed = (now() - last_successful_response.last_checked).total_seconds()
                    elif last_unauthorised_response:
                        time_elapsed = (now() - last_unauthorised_response.last_checked).total_seconds()
                
                data = {
                    'id': latest_response.id,
                    'status_code': latest_response.last_status_code,
                    'timestamp': latest_response.last_checked.isoformat(),
                    'is_online': is_online,
                    'time_elapsed': time_elapsed,
                    'ip_address': iotDevice.ip_address,
                    'mac_address': iotDevice.mac_address,
                    'uptime': iotDevice.uptime,
                    'response_time': f"{latest_response.response_time:.6f}",
                    'response_file': latest_response.response_file.url if latest_response.response_file else None,
                    'current_response': latest_response.current_response,
                }
                
                yield f"data: {json.dumps(data)}\n\n"
                
            yield f": keepalive {now()}\n\n"
            time.sleep(1)

    