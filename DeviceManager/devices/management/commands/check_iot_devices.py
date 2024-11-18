import concurrent.futures
import time
import requests
import logging
import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from devices.models import IoTDevice, IoTDeviceEndpoint, IoTDeviceResponse

logger = logging.getLogger('iot_device_checker')

def save_response_to_json(device_id, endpoint_name, status, response_data):
    directory = os.path.join(settings.BASE_DIR,f"media/iot_responses")
    os.makedirs(directory, exist_ok=True)
    
    filepath = os.path.join(directory,f"{device_id}_{endpoint_name}_{status}.json")

    new_entry = {
        'timestamp': timezone.now().isoformat(),
        'data': response_data
    }
    

    if os.path.exists(filepath) and os.path.getsize(filepath) > 1_000_000:  # 1 MB

        data = {'responses': [new_entry]}
    else:
     
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        else:
            data = {'responses': []}
        data['responses'].insert(0, new_entry)

    with open(filepath, 'w') as f:
        json.dump(data, f)
    
    return filepath


def check_device(iotDevice, endpoint):
    logger.info(f"Checking device: {iotDevice.device.name} (ID: {iotDevice.id}) using endpoint: {endpoint.name}")
    start_time = timezone.now()
    try:
        headers = {
            'Authorization': f'Token {iotDevice.token}',
            'X-IoTDeviceToken': iotDevice.token
        }
        response = requests.request(
            method=endpoint.method,
            url=f"{endpoint.url}?token={iotDevice.token}",
            headers=headers,
            timeout=5
        )

        end_time = timezone.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            status = '200'
            response_data = response.json()
        else:
            status = response.status_code
            response_data = response.text

        last_checked = timezone.now()
        file_path = save_response_to_json(iotDevice.id, endpoint.name, status, response_data)
        

        IoTDeviceResponse.objects.update_or_create(
            device=iotDevice,
            endpoint=endpoint,
            last_status_code=response.status_code,
            defaults={
                'response_time': response_time,
                'response_file': file_path,
                'is_success': response.status_code == 200,
                'last_checked': last_checked,
                'current_response': response_data

            }
        )
        
        if response.status_code == 200:
            
            # Update MAC address and uptime
            iotDevice.mac_address = response_data.get('mac_address', iotDevice.mac_address)
            iotDevice.uptime = response_data.get('uptime', iotDevice.uptime)
            iotDevice.last_checked = last_checked
            iotDevice.save()

            logger.info(f"Device {iotDevice.device.name} (ID: {iotDevice.id}) is online. Response time: {response_time:.2f}s")
            return iotDevice, True, f"Device {iotDevice.device.name} is online"
        else:
            logger.warning(f"Device {iotDevice.device.name} (ID: {iotDevice.id}) returned status code: {response.status_code}")
            return iotDevice, False, f"Device {iotDevice.device.name} returned status code: {response.status_code}"
    
    except requests.RequestException as e:
        end_time = timezone.now()
        response_time = (end_time - start_time).total_seconds()
        last_checked = timezone.now()
        logger.error(f"Error connecting to device {iotDevice.device.name} (ID: {iotDevice.id}): {str(e)}")
        file_path = save_response_to_json(iotDevice.id, endpoint.name, 'error', str(e))
        status_code = 0

        IoTDeviceResponse.objects.update_or_create(
            device=iotDevice,
            endpoint=endpoint,
            last_status_code=status_code,
            defaults={
                'response_time': response_time,
                'response_file': file_path,
                'is_success': False,
                'last_checked': last_checked,
            }
        )
        return iotDevice, False, f"Error connecting to device {iotDevice.device.name}: {str(e)}"

class Command(BaseCommand):
    help = 'Continuously checks all IoT devices at one-minute intervals'

    def handle(self, *args, **options):
        while True:
            start_time = timezone.now()
            
            self.check_all_devices()
            
            elapsed_time = (timezone.now() - start_time).total_seconds()
            sleep_time = max(30 - elapsed_time, 0)

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
