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

    
    if(removeIoTBtn) {
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
    }
 
    if (connectionSettingsBtn) {
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
    }
    
    // Add 'needs-validation' class to the form
    document.getElementById('connectionSettingsForm').classList.add('needs-validation');

    document.getElementById('submitConnectionSettings').addEventListener('click', function(event) {
        const form = document.getElementById('connectionSettingsForm');
        const ipAddress = document.getElementById('newIpAddress');
        const token = document.getElementById('newToken');
        
        // Prevent form from submitting
        event.preventDefault();
        event.stopPropagation();
        
        // Custom validation
        if (!ipAddress.value.trim() && !token.value.trim()) {
            ipAddress.setCustomValidity('Please enter either IP address or token');
            token.setCustomValidity('Please enter either IP address or token');
        } else {
            ipAddress.setCustomValidity('');
            token.setCustomValidity('');
        }
        
        // Trigger Bootstrap validation
        form.classList.add('was-validated');
        
        if (form.checkValidity()) {
            const newIpAddress = ipAddress.value.trim();
            const newToken = token.value.trim();
    
            // Make the request to the server, which will then communicate with the IoT device
            fetch('/api/update_iot_settings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({
                    deviceId: deviceId,
                    ipAddress: newIpAddress,
                    token: newToken,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    bootstrap.Modal.getInstance(document.getElementById('connectionSettingsModal')).hide();
                    showAlertAndReload('IoT settings updated successfully and device is online', 'success');
                } else {
                    throw new Error(data.error || 'Failed to update IoT settings');
                }
            })
            .catch(error => {
                showAlert(error.message || 'An error occurred while updating IoT settings', 'danger');
            });
        }
    });


    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }


});
