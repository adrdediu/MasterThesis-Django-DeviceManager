let ongoingLedCommand = false;
let isOnline = false;

const spinner = document.getElementById('led-spinner');

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

    const tempCtx = document.getElementById('temperatureChart').getContext('2d');
    const pressureCtx = document.getElementById('pressureChart').getContext('2d');
    
    temperatureChart = new TemperatureChart(tempCtx);
    pressureChart = new PressureChart(pressureCtx);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateDeviceStatus(data);
    };

    eventSource.onerror = function(error) {
        console.error('EventSource failed:', error);
        eventSource.close();
    };

    
function updateDeviceStatus(data) {
    isOnline = data.is_online;

    if(isOnline) {
        if(!ongoingLedCommand) {
            enableLedControls();
            spinner.classList.add('d-none');
            document.querySelector('#current-led-pattern .fw-bold').textContent = data.current_response.led_pattern;
            
            // Update badge colors
            updateBadgeColors(data.current_response.led_pattern);
        }
    } else {
        enableLedControls(false);
        document.querySelector('#current-led-pattern .fw-bold').textContent = 'Loading...';
        spinner.classList.remove('d-none');
        
        // Set all badges to secondary when offline
        updateBadgeColors('All Off');
    }

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
            responseTime.textContent = `${Math.floor(data.response_time *1000) || 'N/A'} ms`;
        }
    }


    if (data.current_response && data.current_response.temperature !== undefined) {
        temperatureChart.update(data.current_response.temperature);
    } else {
        temperatureChart.noData();
    }

    if (data.current_response && data.current_response.pressure !== undefined) {
        pressureChart.update(data.current_response.pressure);
    } else {
        pressureChart.noData();
    }
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

function sendLedCommand(iotDeviceId, pattern, static = false) {
    showAlert('Sending LED command...', 'info', false);
    ongoingLedCommand = true;
    enableLedControls(false);
    document.querySelector('#current-led-pattern .fw-bold').textContent = 'Loading...';
    spinner.classList.remove('d-none');

    let url = `/api/iot_device/${iotDeviceId}/setleds/`; 
    let data = {}
    if (pattern) {
        data.pattern = pattern;
        if(!static) {
            const interval = document.getElementById('ledInterval').value;
            if (interval) {
                data.interval = interval;
            }
        } else {
            data.interval = false;
        }
    }

    console.log(url,data)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {

            if (data.success) {
                showAlert(data.message, 'success');
                enableLedControls();
                console.log(data)
                document.querySelector('#current-led-pattern .fw-bold').textContent = data.response.pattern;
                spinner.classList.add('d-none');

                // Update badge colors
                const ledPattern = data.response.pattern;
                updateBadgeColors(ledPattern);
            } else {
                showAlert('LED control operation failed: No pattern received', 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            showAlert('Error controlling LED', 'danger');
        });
}


function enableLedControls(enable = true) {
    const buttons = document.querySelectorAll('.led-control-btn');
    buttons.forEach(btn => btn.disabled = !enable);

}

// Define the updateBadgeColors function
function updateBadgeColors(ledPattern) {
    if (ledPattern === "All On") {
        for (let i = 1; i <= 7; i++) {
            const badge = document.getElementById(`badge-G${i}`);
            if (badge) {
                badge.classList.remove('bg-secondary');
                badge.classList.add('bg-success');
            }
        }
    } else if (ledPattern === "All Off" || ledPattern === "None") {
        for (let i = 1; i <= 7; i++) {
            const badge = document.getElementById(`badge-G${i}`);
            if (badge) {
                badge.classList.remove('bg-success');
                badge.classList.add('bg-secondary');
            }
        }
    } else {
        const activeGroups = ledPattern.split(' ');
        for (let i = 1; i <= 7; i++) {
            const badge = document.getElementById(`badge-G${i}`);
            if (badge) {
                if (activeGroups.includes(`G${i}`)) {
                    badge.classList.remove('bg-secondary');
                    badge.classList.add('bg-success');
                } else {
                    badge.classList.remove('bg-success');
                    badge.classList.add('bg-secondary');
                }
            }
        }
    }
}