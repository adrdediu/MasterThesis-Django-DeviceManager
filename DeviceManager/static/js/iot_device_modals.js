document.addEventListener('DOMContentLoaded', function() {
    const activateIoTBtn = document.getElementById('activateIoTBtn');
    const connectionSettingsBtn = document.getElementById('connectionSettingsBtn');
    const removeIoTBtn = document.getElementById('removeIoTBtn');
    const iotStatusBadge = document.getElementById('iotStatusBadge');
    const deviceId = document.getElementById('device-id').dataset.deviceId;


    document.getElementById('submitActivateIoT').addEventListener('click', function() {
        const ipAddress = document.getElementById('ipAddress').value;
        const token = document.getElementById('token').value;

        fetch('/api/activate_iot_features/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                deviceId: deviceId,
                ipAddress: ipAddress,
                token: token
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                
                bootstrap.Modal.getInstance(document.getElementById('activateIoTModal')).hide();
                showAlertAndReload('IoT features activated successfully', 'success');
            } else {
                showAlert('Failed to activate IoT features: ' + data.error, 'danger');
            }
        })
        .catch(error => {
            showAlert('An error occurred while activating IoT features', 'danger');
        });
    });

    removeIoTBtn.addEventListener('click', function() {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, remove IoT features!'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch('/api/remove_iot_features/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({
                        deviceId: deviceId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        
                        showAlertAndReload('IoT features have been removed.', 'success');
                    } else {
                        Swal.fire(
                            'Error!',
                            'Failed to remove IoT features: ' + data.error,
                            'error'
                        );
                    }
                })
                .catch(error => {
                    Swal.fire(
                        'Error!',
                        'An error occurred while removing IoT features',
                        'error'
                    );
                });
            }
        });
    });

 
    
    connectionSettingsBtn.addEventListener('click', function() {
        fetch(`/api/get_iot_settings/${deviceId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentIpAddress').value = data.ipAddress;
            document.getElementById('currentToken').value = data.token;
        })
        .catch(error => {
            showAlert('An error occurred while fetching IoT settings', 'danger');
        });
    });
    

    document.getElementById('submitConnectionSettings').addEventListener('click', function() {
        const ipAddress = document.getElementById('currentIpAddress').value;
        const token = document.getElementById('currentToken').value;
        
        fetch('/api/update_iot_settings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                deviceId: deviceId,
                ipAddress: ipAddress,
                token: token,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                bootstrap.Modal.getInstance(document.getElementById('connectionSettingsModal')).hide();
                showAlertAndReload ('IoT settings updated successfully', 'success');
            } else {
                showAlert('Failed to update IoT settings: ' + data.error, 'danger');
            }
        })
        .catch(error => {
            showAlert('An error occurred while updating IoT settings', 'danger');
        });
    });

    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }


});
