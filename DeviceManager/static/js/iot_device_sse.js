document.addEventListener('DOMContentLoaded', function() {
    const deviceId = document.getElementById("device-id").getAttribute("data-device-id");
    console.log(deviceId);
    const eventSource = new EventSource(`/sse/${deviceId}/`);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const isOnline = data.status_code >= 200 && data.status_code < 300;
        document.getElementById('iotDeviceStatus').className = isOnline ? 'badge bg-success' : 'badge bg-danger';
        document.getElementById('iotDeviceStatus').innerHTML = `<i class="bi bi-circle-fill me-1"></i> ${isOnline ? 'Online' : 'Offline'}`;

        const lastResponseElement = document.querySelector('#iotDeviceStatus + div small');
        if (lastResponseElement) {
            lastResponseElement.innerHTML = `<i class="bi bi-clock"></i> Last response: ${formatTimeElapsed(data.time_elapsed)} ago`;
        }
    };

    eventSource.onerror = function(error) {
        console.error('EventSource failed:', error);
        eventSource.close();
    };

    function formatTimeElapsed(seconds) {
        if (seconds === null) return 'N/A';
        if (seconds < 60) return `${Math.floor(seconds)} seconds`;
        
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
    

});