document.addEventListener('DOMContentLoaded', function() {
    const deviceId = document.getElementById("device-id").getAttribute("data-device-id");
    const eventSource = new EventSource(`/sse/${deviceId}/`);
   
    // Get UI Components
    const statusBadge = document.getElementById('iotDeviceStatus');
    const ipAddress = document.getElementById('iotIpAddress');
    const macAddress = document.getElementById('iotMacAddress');
    const statusCode = document.getElementById('iotStatusCode');
    const lastSeen = document.querySelector('#iotLastSeen');
    const uptime = document.getElementById('iotUptime');
    const responseTime = document.getElementById('iotResponseTime');

    

        

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateDeviceStatus(data);
    };

    eventSource.onerror = function(error) {
        console.error('EventSource failed:', error);
        eventSource.close();
    };

    function updateDeviceStatus(data) {
        const isOnline = data.is_online;

        // Update status
        statusBadge.className = isOnline ? 'badge bg-success' : 'badge bg-danger';
        statusBadge.innerHTML = `<i class="bi bi-circle-fill me-1"></i> ${isOnline ? 'Online' : 'Offline'}`;

        // Update IP and MAC
        ipAddress.textContent = data.ip_address || 'N/A';
        macAddress.textContent = data.mac_address || 'N/A';

        // Update status code
        statusCode.textContent = data.status_code || 'N/A';
        statusCode.className = `badge ${data.status_code === 200 ? 'bg-success' : 'bg-danger'}`;

        // Update last seen
        if (lastSeen) {
            lastSeen.textContent = formatTimeElapsed(data.time_elapsed);
        }
        if(data.status_code){


            // Update uptime
            if (uptime) {
                uptime.textContent = formatUptime(data.uptime);
            }

            // Update response time
            if (responseTime) {
                console.log(data.response_time);
                responseTime.textContent = `${Math.floor(data.response_time *1000) || 'N/A'} ms`;
            }

        }

        if ((data.current_response.temperature)&&(data.current_response.pressure)){

        }

        //updateTemperature(data.temperature);
        //updatePressure(data.pressure);

    }

    

    function formatTimeElapsed(seconds) {
        if (seconds === null) return 'N/A';
        if (seconds < 60) return `${Math.floor(seconds)} secs`;
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        
        if (minutes < 60) {
            return `${minutes} min${minutes !== 1 ? 's' : ''} ${remainingSeconds} sec${remainingSeconds !== 1 ? 's' : ''}`;
        }
        
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        
        if (hours < 24) {
            return `${hours} hour${hours !== 1 ? 's' : ''} ${remainingMinutes} min${remainingMinutes !== 1 ? 's' : ''}`;
        }
        
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;
        
        return `${days} day${days !== 1 ? 's' : ''} ${remainingHours} hour${remainingHours !== 1 ? 's' : ''}`;
    }

    function formatUptime(seconds) {
        if (seconds === null) return 'N/A';
        return formatTimeElapsed(seconds);
    }
});
