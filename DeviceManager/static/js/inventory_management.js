document.addEventListener('DOMContentLoaded', function() {

    const showCurrentInventory = document.getElementById('showCurrentInventory');
    const showInventorizationLists = document.getElementById('showInventorizationLists');
    const saveDisplayPreferences = document.getElementById('saveDisplayPreferences');

    // Load saved preferences
    loadDisplayPreferences();

    // Toggle visibility
    showCurrentInventory.addEventListener('change', () => toggleVisibility('currentInventoryCard', showCurrentInventory.checked));
    showInventorizationLists.addEventListener('change', () => toggleVisibility('inventorizationListsCard', showInventorizationLists.checked));

    // Save preferences
    saveDisplayPreferences.addEventListener('click', savePreferences);

    function toggleVisibility(cardId, isVisible) {
        document.getElementById(cardId).style.display = isVisible ? 'block' : 'none';
    }

    function savePreferences() {
        localStorage.setItem('showCurrentInventory', showCurrentInventory.checked);
        localStorage.setItem('showInventorizationLists', showInventorizationLists.checked);
        showAlert('Display preferences saved!', 'success');
    }

    function loadDisplayPreferences() {
        showCurrentInventory.checked = localStorage.getItem('showCurrentInventory') !== 'false';
        showInventorizationLists.checked = localStorage.getItem('showInventorizationLists') !== 'false';

        toggleVisibility('currentInventoryCard', showCurrentInventory.checked);
        toggleVisibility('inventorizationListsCard', showInventorizationLists.checked);
    }


    // Pause/Resume
    document.querySelectorAll('.pause-resume').forEach(btn => {
        btn.addEventListener('click', function() {
            const inventoryId = this.getAttribute('data-inventory-id');
            const action = this.getAttribute('data-action');
            pauseResumeInventory(inventoryId, action, this);
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

});
