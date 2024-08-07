import concurrent.futures
import requests
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from devices.models import IoTDevice, IoTDeviceEndpoint,IoTDeviceResponse

logger = logging.getLogger('iot_device_checker')

import time
import requests

def check_device(iotDevice, endpoint):
    logger.info(f"Checking device: {iotDevice.device.name} (ID: {iotDevice.id}) using endpoint: {endpoint.name}")
    start_time = time.time()
    try:
        headers = {
            'Authorization': f'Token {iotDevice.token}',
            'X-IoTDeviceToken': iotDevice.token
        }
        response = requests.request(
            method=endpoint.method,
            url=f"http://{iotDevice.ip_address}{endpoint.url}?token={iotDevice.token}",
            headers=headers,
            timeout=5
        )
        
        response_time = time.time() - start_time
        
        IoTDeviceResponse.objects.create(
            device=iotDevice,
            endpoint=endpoint,
            status_code=response.status_code,
            response_time=response_time,
            response_data=response.json() if response.status_code == 200 else None,
            error_message=None if response.status_code == 200 else response.text
        )
        
        if response.status_code == 200:
            logger.info(f"Device {iotDevice.device.name} (ID: {iotDevice.id}) is online. Response time: {response_time:.2f}s")
            return iotDevice, True, f"Device {iotDevice.device.name} is online"
        else:
            logger.warning(f"Device {iotDevice.device.name} (ID: {iotDevice.id}) returned status code: {response.status_code}")
            return iotDevice, False, f"Device {iotDevice.device.name} returned status code: {response.status_code}"
    
    except requests.RequestException as e:
        response_time = time.time() - start_time
        logger.error(f"Error connecting to device {iotDevice.device.name} (ID: {iotDevice.id}): {str(e)}")
        IoTDeviceResponse.objects.create(
            device=iotDevice,
            endpoint=endpoint,
            status_code=0,
            response_time=response_time,
            response_data=None,
            error_message=str(e)
        )
        return iotDevice, False, f"Error connecting to device {iotDevice.device.name}: {str(e)}"

class Command(BaseCommand):
    help = 'Continuously checks all IoT devices at one-minute intervals'

    def handle(self, *args, **options):
        while True:
            start_time = time.time()
            
            self.check_all_devices()
            

            elapsed_time = time.time() - start_time
            sleep_time = max(1 - elapsed_time, 0)

            logger.info(f"Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)

    def check_all_devices(self):
        logger.info("Starting IoT device check")
        iotDevices = IoTDevice.objects.all().prefetch_related('endpoints')
        logger.info(f"Found {iotDevices.count()} iotDevices to check")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for iotDevice in iotDevices:
                status_endpoint = iotDevice.endpoints.filter(name='status').first()
                if status_endpoint:
                    futures.append(executor.submit(check_device, iotDevice, status_endpoint))
                else:
                    logger.warning(f"No status endpoint found for iotDevice {iotDevice.device.name} (ID: {iotDevice.id})")
            
            for future in concurrent.futures.as_completed(futures):
                iotDevice, is_online, message = future.result()
                
                if is_online:
                    logger.info(message)
                else:
                    logger.error(message)
                
                IoTDevice.objects.filter(pk=iotDevice.pk).update(is_online=is_online, last_checked=timezone.now())

                logger.info(f"Updated status for device {iotDevice.device.name} (ID: {iotDevice.id}): is_online={is_online}, last_checked={iotDevice.last_checked}")

        logger.info("Finished checking all devices")