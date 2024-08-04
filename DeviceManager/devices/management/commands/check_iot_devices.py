import concurrent.futures
import requests
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from devices.models import IoTDevice, IoTDeviceEndpoint,IoTDeviceResponse

logger = logging.getLogger('iot_device_checker')

import time
import requests

def check_device(device, endpoint):
    logger.info(f"Checking device: {device.name} (ID: {device.id}) using endpoint: {endpoint.name}")
    start_time = time.time()
    try:
        headers = {
            'Authorization': f'Token {device.token}',
            'X-IoTDeviceToken': device.token
        }
        response = requests.request(
            method=endpoint.method,
            url=f"http://{device.ip_address}{endpoint.url}?token={device.token}",
            headers=headers,
            timeout=5
        )
        
        response_time = time.time() - start_time
        
        IoTDeviceResponse.objects.create(
            device=device,
            endpoint=endpoint,
            status_code=response.status_code,
            response_time=response_time,
            response_data=response.json() if response.status_code == 200 else None,
            error_message=None if response.status_code == 200 else response.text
        )
        
        if response.status_code == 200:
            logger.info(f"Device {device.name} (ID: {device.id}) is online. Response time: {response_time:.2f}s")
            return device, True, f"Device {device.name} is online"
        else:
            logger.warning(f"Device {device.name} (ID: {device.id}) returned status code: {response.status_code}")
            return device, False, f"Device {device.name} returned status code: {response.status_code}"
    
    except requests.RequestException as e:
        response_time = time.time() - start_time
        logger.error(f"Error connecting to device {device.name} (ID: {device.id}): {str(e)}")
        IoTDeviceResponse.objects.create(
            device=device,
            endpoint=endpoint,
            status_code=0,
            response_time=response_time,
            response_data=None,
            error_message=str(e)
        )
        return device, False, f"Error connecting to device {device.name}: {str(e)}"

class Command(BaseCommand):
    help = 'Checks all IoT devices in the database concurrently'

    def handle(self, *args, **options):
        logger.info("Starting IoT device check")
        devices = IoTDevice.objects.all().prefetch_related('endpoints')
        logger.info(f"Found {devices.count()} devices to check")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for device in devices:
                status_endpoint = device.endpoints.filter(name='status').first()
                if status_endpoint:
                    futures.append(executor.submit(check_device, device, status_endpoint))
                else:
                    logger.warning(f"No status endpoint found for device {device.name} (ID: {device.id})")
            
            for future in concurrent.futures.as_completed(futures):
                device, is_online, message = future.result()
                
                if is_online:
                    logger.info(message)
                else:
                    logger.error(message)
                
                device.is_online = is_online
                device.last_checked = timezone.now()
                device.save()
                logger.info(f"Updated status for device {device.name} (ID: {device.id}): is_online={is_online}, last_checked={device.last_checked}")

        logger.info("Finished checking all devices")
