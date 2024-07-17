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
            populateEditForm(data.device);
            var editDeviceModal = new bootstrap.Modal(document.getElementById('editDeviceModal'));
            editDeviceModal.show();
        } else {
            Swal.fire('Error', data.message || 'Failed to load device data', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error', 'An unexpected error occurred', 'error');
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
            if (option.dataset[parentAttribute] === parentValue.toString()) {
                option.style.display = '';
            } else {
                option.style.display = 'none';
            }
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
    });

    document.getElementById('editDeviceFloorModal').addEventListener('change', function() {
        updateOptions('editDeviceRoomModal', 'floor', this.value);
        document.getElementById('editDeviceRoomModal').value = '';
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
                    Swal.fire('Success', 'Device updated successfully', 'success').then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire('Error', data.message || 'Failed to update device', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire('Error', 'An unexpected error occurred', 'error');
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
    
    
    // Function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

})