document.addEventListener('DOMContentLoaded', function() {

    const showCurrentInventory = document.getElementById('showCurrentInventory');
    const showInventorizationLists = document.getElementById('showInventorizationLists');
    const showInventoryHistory = document.getElementById('showInventoryHistory');
    const saveDisplayPreferences = document.getElementById('saveDisplayPreferences');

    // Load saved preferences
    loadDisplayPreferences();

    // Toggle visibility
    showCurrentInventory.addEventListener('change', () => toggleVisibility('currentInventoryCard', showCurrentInventory.checked));
    showInventorizationLists.addEventListener('change', () => toggleVisibility('inventorizationListsCard', showInventorizationLists.checked));
    showInventoryHistory.addEventListener('change', () => toggleVisibility('inventoryHistoryCard', showInventoryHistory.checked));

    // Save preferences
    saveDisplayPreferences.addEventListener('click', savePreferences);

    function toggleVisibility(cardId, isVisible) {
        document.getElementById(cardId).style.display = isVisible ? 'block' : 'none';
    }

    function savePreferences() {
        localStorage.setItem('showCurrentInventory', showCurrentInventory.checked);
        localStorage.setItem('showInventorizationLists', showInventorizationLists.checked);
        localStorage.setItem('showInventoryHistory', showInventoryHistory.checked);
        alert('Display preferences saved!');
    }

    function loadDisplayPreferences() {
        showCurrentInventory.checked = localStorage.getItem('showCurrentInventory') !== 'false';
        showInventorizationLists.checked = localStorage.getItem('showInventorizationLists') !== 'false';
        showInventoryHistory.checked = localStorage.getItem('showInventoryHistory') !== 'false';

        toggleVisibility('currentInventoryCard', showCurrentInventory.checked);
        toggleVisibility('inventorizationListsCard', showInventorizationLists.checked);
        toggleVisibility('inventoryHistoryCard', showInventoryHistory.checked);
    }


    // Pause/Resume
    document.querySelectorAll('.pause-resume').forEach(btn => {
        btn.addEventListener('click', function() {
            const inventoryId = this.getAttribute('data-inventory-id');
            const action = this.getAttribute('data-action');
            pauseResumeInventory(inventoryId, action, this);
        });
    });

    // Add event listeners for the new Generate Report buttons
    document.querySelectorAll('.generate-report').forEach(btn => {
        btn.addEventListener('click', function() {
            const inventoryId = this.getAttribute('data-inventory-id');
            generateReport(inventoryId);
        });
    });

    // Cancel
    document.querySelectorAll('.cancel').forEach(btn => {
        btn.addEventListener('click', function() {
            const inventoryId = this.getAttribute('data-inventory-id');
            cancelInventory(inventoryId);
        });
    });


    



    // Start Inventory
    const startInventoryBtn = document.getElementById('startInventory');
    const startInventoryModal = document.getElementById('startInventoryModal');
    let startInventoryModalInstance = null;

    if (startInventoryBtn && startInventoryModal) {
        startInventoryBtn.addEventListener('click', function() {
            if (!startInventoryModalInstance) {
                startInventoryModalInstance = new bootstrap.Modal(startInventoryModal);
            }
            startInventoryModalInstance.show();
        });
    }

    // Confirm Start Inventory
    document.getElementById('confirmStartInventory').addEventListener('click',function() {
        let inventoryId = this.getAttribute('data-inventory-id');
        startInventory(inventoryId);
    })

    function startInventory(inventoryId) {

        fetch('/inventory/start/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                inventory_id : inventoryId
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Inventory started successfully','success');
                if (startInventoryModalInstance) {
                    startInventoryModalInstance.hide();
                }
                showConfirmation(
                    'Inventory started successfully!',
                    'Do you want to view the inventory details?',
                    'Yes, view details',
                    'No, return to list',
                    'success',
                ).then(result => {
                    if (result.isConfirmed) {
                        window.location.href = `/inventory/${data.inventory_list_id}`;
                    } else {
                        window.location.href = `/inventory/management/${data.inventory_id}`;
                    }
                });
            } else {
                showAlert(data.message || 'Failed to start inventory','danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred while starting the inventory','danger');
        });
    }

    function pauseResumeInventory(inventoryId, action) {
    showConfirmation(
        'Confirm Action',
        `Are you sure you want to ${action} this inventory?`,
        `Yes, ${action} it!`,
        'Cancel'
    ).then((result) => {
        if (result.isConfirmed) {
            fetch('/inventory/pause-resume/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    inventory_id: inventoryId,
                    action: action
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlertAndReload(`Inventory ${action}d successfully`, 'success');
                } else {
                    showAlertAndReload(data.message || `Failed to ${action} inventory`, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert(`An error occurred while ${action}ing the inventory`, 'error');
            });
        }
    });
}

    function cancelInventory(inventoryId) {
        showConfirmation(
            'Cancel Inventory',
            'Are you sure you want to cancel this inventory? This action cannot be undone.',
            'Yes, cancel it!',
            'No, keep it'
        ).then((result) => {
            if (result.isConfirmed) {
                fetch('/inventory/cancel/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        inventory_id: inventoryId
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showAlertAndReload('Inventory canceled successfully','success');
                    } else {
                        showAlert(data.message || 'Failed to cancel inventory', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('An error occurred while canceling the inventory', 'error');
                });
            }
        });
    }


    function generateReport(inventoryId) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/api/inventory/${inventoryId}/generate-report/`;
        
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = getCookie('csrftoken');
        form.appendChild(csrfInput);

        const typeInput = document.createElement('input');
        typeInput.type = 'hidden';
        typeInput.name = 'report_type';
        typeInput.value = 'pdf'; // You can change this to 'excel' if needed

        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    }

  
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        console.log(cookieValue);
        return cookieValue;
    }
});
