document.addEventListener('DOMContentLoaded', function() {

    // Add Device form submission
    const addDeviceForm = document.getElementById('addDeviceForm');
    if (addDeviceForm) {
        addDeviceForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch('/api/devices/add_device/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {

                    
                    // Close the Add Device modal
                    var addDeviceModal = bootstrap.Modal.getInstance(document.getElementById('addDeviceModal'));
                    addDeviceModal.hide();
                    showConfirmation(
                        'Device Added',
                        'Do you want to view the added device details?',
                        'Yes, view details',
                        'No, return to list',
                        'success',
                    ).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = `/device/${data.device_pk}/`;
                        } else {
                            location.reload();
                        }
                    });


                } else if (data.error) {
                    showAlert(data.error, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error)
                showAlert('Something went wrong. Please try again.', 'danger');
            });
        });
    }

    // Category and subcategory handling in the modal
    const deviceCategoryModal = document.getElementById('deviceCategoryModal');
    if (deviceCategoryModal) {
        deviceCategoryModal.addEventListener('change', function() {
            selectorHandler([deviceCategoryModal, document.getElementById('deviceSubcategoryModal')], "/get_subcategories/?category_id", ["Category", "Subcategory"], true);
        });
    }

    // Building, floor, and room handling in the modal
    const deviceBuildingModal = document.getElementById('deviceBuildingModal');
    const deviceFloorModal = document.getElementById('deviceFloorModal');
    if (deviceBuildingModal) {
        deviceBuildingModal.addEventListener('change', function() {
            selectorHandler([deviceBuildingModal, deviceFloorModal, document.getElementById('deviceRoomModal')], "/get_floors/?building_id", ["Building", "Floor", "Room"], true);
        });
    }
    if (deviceFloorModal) {
        deviceFloorModal.addEventListener('change', function() {
            selectorHandler([deviceFloorModal, document.getElementById('deviceRoomModal')], "/get_rooms/?floor_id", ["Floor", "Room"], true);
        });
    }

        // Selector handlers
    function selectorHandler(selectors, url, modelNames, detailed_options) {
        for (var i = 1; i < selectors.length; i++) {
            if (detailed_options)
                selectors[i].innerHTML = `<option value="">Select a ${modelNames[0]} first</option>`;
            else
                selectors[i].innerHTML = `<option value="">All</option><option value="">Choose a ${modelNames[0]} first...</option>`;
        }

        let value = selectors[0].value;
        if(value){
            fetch(`${url}=${value}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (!(Array.isArray(data) && data.length === 0)) {
                    if (detailed_options)
                        selectors[1].innerHTML = `<option value="">Select a ${modelNames[1]}</option>`;
                    else 
                        selectors[1].innerHTML = `<option value="">All</option><o value="">Choose a ${modelNames[1]} first...</o`;

                    for (var i = 2; i < selectors.length; i++) {
                        if (detailed_options) 
                            selectors[i].innerHTML = `<option value="">Please select a ${modelNames[i-1]} first.</option>`;
                        else
                            selectors[i].innerHTML = `<option value="">All</option><option value="">Choose a ${modelNames[i-1]} first...</option>`;
                    }
                    data.forEach(model => {
                        selectors[1].innerHTML += `<option value="${model.id}">${model.name}</option>`;
                    });
                } else {
                    if (detailed_options)
                        selectors[1].innerHTML = `<option value="">Please add a ${modelNames[1]} first</option>`;
                }
            })
            .catch(error => console.error('Error:', error));
        } 
    }

    // Edit Device
    document.querySelectorAll('.edit-device').forEach(btn => {
        btn.addEventListener('click', function() {
            const deviceId = this.getAttribute('data-device-id');
            editDevice(deviceId);
        });
    });


    // Edit Device - Add reset functionality
    document.getElementById('resetEditForm').addEventListener('click', function() {
        if (window.editingDevice) {
            populateEditForm(window.editingDevice);
        }
    });

    // Edit Device Function - Get Device Data
    function editDevice(deviceId) {
        fetch(`/api/devices/edit/?device_id=${deviceId}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            window.editingDevice = data.device;
        
            var editDeviceModal = new bootstrap.Modal(document.getElementById('editDeviceModal'));
            populateEditForm(window.editingDevice);
            editDeviceModal.show();
        } else {
            showAlert('Error', data.message || 'Failed to load device data', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error', 'An unexpected error occurred', 'danger');
    });
    }
    
    // Edit Device Function - Populate Form
    function populateEditForm(device) {
        document.getElementById('editDeviceId').value = device.id;
        document.getElementById('editDeviceName').value = device.name;
        document.getElementById('editDeviceDescription').value = device.description;
        document.getElementById('editDeviceSerialNumber').value = device.serial_number;
        
        const categorySelect = document.getElementById('editDeviceCategoryModal');
        categorySelect.value = device.category;
        updateOptions('editDeviceSubcategoryModal', 'category', device.category);
        
        const buildingSelect = document.getElementById('editDeviceBuildingModal');
        buildingSelect.value = device.building;
        updateOptions('editDeviceFloorModal', 'building', device.building);
        
        document.getElementById('editDeviceSubcategoryModal').value = device.subcategory;
        document.getElementById('editDeviceFloorModal').value = device.floor;

        updateOptions('editDeviceRoomModal', 'floor', device.floor);
        document.getElementById('editDeviceRoomModal').value = device.room;
    }
    
    // Edit Device Function - Update Form Options
    function updateOptions(selectId, parentAttribute, parentValue) {
        const select = document.getElementById(selectId);
        Array.from(select.options).forEach(option => {
            option.style.display = option.dataset[parentAttribute] === parentValue.toString() ? '' : 'none';
        });
    }

    // Edit Device Function - Update Form Options - Listener
    document.getElementById('editDeviceCategoryModal').addEventListener('change', function() {
        updateOptions('editDeviceSubcategoryModal', 'category', this.value);
        document.getElementById('editDeviceSubcategoryModal').value = '';
    });

    document.getElementById('editDeviceBuildingModal').addEventListener('change', function() {
        updateOptions('editDeviceFloorModal', 'building', this.value);
        document.getElementById('editDeviceFloorModal').value = '';
        document.getElementById('editDeviceRoomModal').value = '';
        document.getElementById('editDeviceRoomModal').options[0].text = 'Select a Floor first...';
    });

    document.getElementById('editDeviceFloorModal').addEventListener('change', function() {
        updateOptions('editDeviceRoomModal', 'floor', this.value);
        document.getElementById('editDeviceRoomModal').value = '';
        document.getElementById('editDeviceRoomModal').options[0].text = 'Select a Room';
    });

    // Edit Device form submission
    const editDeviceForm = document.getElementById('editDeviceForm');
    if (editDeviceForm) {
        editDeviceForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch('/api/devices/edit/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlertAndReload( 'Device updated successfully','success');
                } else {
                    showAlert(data.message || 'Failed to update device', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert(data.message || 'Failed to update device', 'danger');
            });
        });
    }

    // Delete Device
    document.querySelectorAll('.delete-device').forEach(btn => {
        btn.addEventListener('click', function() {
            const deviceId = this.getAttribute('data-device-id');
            deleteDevice(deviceId);
        });
    });

    // Delete Device function
    function deleteDevice(device_id) {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/api/devices/delete_device/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'device_id': device_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire(
                            'Deleted!',
                            'The device has been deleted.',
                            'success'
                        ).then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire(
                            'Error!',
                            data.message || 'An error occurred while deleting the device.',
                            'error'
                        );
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire(
                        'Error!',
                        'An error occurred while deleting the device.',
                        'error'
                    );
                });
            }
        });
    }

    //////////////// QR Code Generation //////////////
        // QR Code regeneration
        var regenerateButton = document.getElementById('regenerateQRCode');

        function handleQRCodeGeneration(action,deviceId) {
            fetch(`/api/device/${deviceId}/qrcode/${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlertAndReload('QR code successfully '+ action + 'd!','success');
                } else {
                    showAlert('Failed to ' + action + ' QR code: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred while ' + action + 'ing the QR code', 'error');
            });
        }
    
        if (regenerateButton) {
            regenerateButton.addEventListener('click', function() {
                const deviceId = this.getAttribute("data-device-id");
                showConfirmation('Regenerate QR Code', 'Are you sure you want to regenerate the QR code?', 'Yes, regenerate it', 'Cancel')
                .then((result) => {
                    if (result.isConfirmed) {
                        handleQRCodeGeneration('regenerate',deviceId);
                    }
                });
            });
        }
    
    
        // Add event listener for the download QR code button
        const downloadQRCodeBtn = document.getElementById('downloadQRCodeBtn');
        if (downloadQRCodeBtn) {
          downloadQRCodeBtn.addEventListener('click', function(event) {
              event.preventDefault();
              
              showConfirmation('Download QR Code', 'Are you sure you want to download the QR code?', 'Yes, download it', 'Cancel')
              .then((result) => {
                  if (result.isConfirmed) {
                      showAlert('Preparing QR code for download...', 'info');
                      
                      fetch(this.href)
                          .then(response => {
                              if (response.ok) {
                                  // Trigger the download
                                  window.location.href = this.href;
                                  showAlert('QR code downloaded successfully!', 'success');
                              } else {
                                  return response.json().then(data => {
                                      throw new Error(data.error || 'Unknown error occurred');
                                  });
                              }
                          })
                          .catch(error => {
                              console.error('Error:', error);
                              if (error.message === 'Device not found') {
                                  showAlert('Device not found. Please check if the device exists.', 'error');
                              } else if (error.message === 'Failed to fetch QR code image') {
                                  showAlert('Failed to download QR code. Please regenerate it.', 'error');
                              } else {
                                  showAlert('An unexpected error occurred. Please try again later.', 'error');
                              }
                          });
                  }
              });
          });
      }
    
    
    
    
    // Function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

})
