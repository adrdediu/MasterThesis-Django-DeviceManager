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


    // View Details
    document.querySelectorAll('.view-details').forEach(btn => {
        btn.addEventListener('click', function() {
            const inventoryId = this.getAttribute('data-inventory-id');
            fetchInventoryDetails(inventoryId);
        });
    });

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


    
    // Initialize DataTable
    let table = new DataTable('#inventorizationTable', {
        responsive: true,
        pageLength: 10,
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        dom: '<"row"<"col-12 col-lg-6 text-center text-lg-start mb-1"li><"col-12 col-lg-6 d-flex justify-content-center justify-content-lg-end p-0 mb-1"p>>rt<"clear">',
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search...",
            lengthMenu: "Show _MENU_ per page",
            paginate: {
                first: "First",
                last: "Last",
                next: ">",
                previous: "<"
            }
        },
        order:[[0,'desc']],
        orderCellsTop: true,
        scrollX: true,
        autoWidth: true,
        columnDefs: [
            { width: '40px', targets: 0 },   // ID
            { width: '100px', targets: 1 },  // Creator
            { width: '100px', targets: 2 },  // Start Date
            { width: '50px', targets: 3 },   // Status
            
            { width: '80px', targets: 5 },   // Scope
            { width: '150px', targets: 6, orderable: false }  // Actions
        ],
        initComplete: function (settings, json) {
            this.api().columns().every(function (index) {
                let column = this;
                let input = document.querySelector('.search-row th:nth-child(' + (index + 1) + ') input, .search-row th:nth-child(' + (index + 1) + ') select');
                if (input) {
                    input.addEventListener('keyup', () => {
                        if (column.search() !== input.value) {
                            column.search(input.value).draw();
                        }
                    });
                    input.addEventListener('change', () => {
                        if (column.search() !== input.value) {
                            column.search(input.value).draw();
                        }
                    });
                }
            });
        }
    });

    let historyTable = new DataTable("#historyTable", {
        perPage: 10,
        perPageSelect: [5, 10, 15, 20],
        searchable: true,
        sortable: true,
        fixedHeight: false,
        labels: {
            placeholder: "Search...",
            perPage: "{select} entries per page",
            noRows: "No entries found",
            info: "Showing {start} to {end} of {rows} entries",
        }
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
    document.getElementById('confirmStartInventory').addEventListener('click', startInventory);

    function startInventory() {
        const buildingId = document.getElementById('buildingSelect').value;
        const scope = document.getElementById('scopeSelect').value;
        
        if (!buildingId) {
            //alert('Please select a building.');
            showAlert('Please select a building.','warning');
            
            return;
        }

        let selectedRooms = [];
        if (scope === 'PARTIAL') {
            selectedRooms = Array.from(document.querySelectorAll('.room-checkbox:checked')).map(cb => cb.dataset.roomId);
            if (selectedRooms.length === 0) {
                showAlert('Please select at least one room for partial inventory.','warning');
                return;
            }
        } else {
            // If scope is ENTIRE, select all rooms in the building
            selectedRooms = 'all'
        }

        const inventoryData = {
            building_id: buildingId,
            room_ids: selectedRooms,
            scope: scope
        };

        fetch('{% url "api_start_inventory" %}', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inventoryData),
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
                        window.location.href = '{% url "inventory_detail" pk=0 %}'.replace('0', data.inventory_id);
                    } else {
                         window.location.href = '{% url "inventory_management" %}';
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


    const buildingSelect = document.getElementById('buildingSelect');
    const scopeSelect = document.getElementById('scopeSelect');
    const partialSelection = document.getElementById('partialSelection');
    const selectAllFloors = document.getElementById('selectAllFloors');
    const floorsList = document.getElementById('floorsList');

    buildingSelect.addEventListener('change', loadFloors);
    scopeSelect.addEventListener('change', togglePartialSelection);
    selectAllFloors.addEventListener('change', toggleAllFloors);
    
    function togglePartialSelection() {
        partialSelection.style.display = scopeSelect.value === 'PARTIAL' ? 'block' : 'none';
        if (scopeSelect.value === 'PARTIAL' && buildingSelect.value) {
            loadFloors();
        }
    }

    function toggleAllFloors(e) {
        const isChecked = e.target.checked;
        const allRoomsCheckboxes = document.querySelectorAll('.select-all-rooms');
        const roomCheckboxes = document.querySelectorAll('.room-checkbox');

        allRoomsCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });

        roomCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });

        updateAllFloorsStatus();
    }

    
    function loadFloors() {
        const buildingId = buildingSelect.value;
        floorsList.innerHTML = '';
        selectAllFloors.checked = false;

        if (buildingId && scopeSelect.value === 'PARTIAL') {
            fetch(`{% url 'get_floors' %}?building_id=${buildingId}`)
                .then(response => response.json())
                .then(floors => {
                    const accordion = document.createElement('div');
                    accordion.className = 'accordion';
                    accordion.id = 'floorsAccordion';

                    floors.forEach((floor, index) => {
                        const floorItem = document.createElement('div');
                        floorItem.className = 'accordion-item';
                        floorItem.innerHTML = `
                            <h2 class="accordion-header" id="heading${floor.id}">
                                <button class="accordion-button ${index === 0 ? '' : 'collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${floor.id}" aria-expanded="${index === 0 ? 'true' : 'false'}" aria-controls="collapse${floor.id}">
                                    ${floor.name}
                                    <div class="ms-auto">
                                        <div class="form-check">
                                            <input class="form-check-input select-all-rooms" type="checkbox" id="selectAllRooms${floor.id}" data-floor-id="${floor.id}">
                                            <label class="form-check-label" for="selectAllRooms${floor.id}">
                                                All Rooms
                                            </label>
                                        </div>
                                    </div>
                                </button>
                            </h2>
                            <div id="collapse${floor.id}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" aria-labelledby="heading${floor.id}" data-bs-parent="#floorsAccordion">
                                <div class="accordion-body">
                                    <div id="roomsList${floor.id}">
                                        <!-- Rooms will be dynamically added here -->
                                    </div>
                                </div>
                            </div>
                        `;
                        accordion.appendChild(floorItem);

                        const selectAllRooms = floorItem.querySelector(`#selectAllRooms${floor.id}`);
                        selectAllRooms.addEventListener('change', (e) => toggleAllRooms(e, floor.id));
                        
                        loadRooms(floor.id);
                    });

                    floorsList.appendChild(accordion);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while loading floors');
                });
        }
    }

    function loadRooms(floorId) {
        fetch(`{% url 'get_rooms' %}?floor_id=${floorId}`)
            .then(response => response.json())
            .then(rooms => {
                const roomsList = document.getElementById(`roomsList${floorId}`);
                roomsList.innerHTML = '';
                rooms.forEach(room => {
                    const roomDiv = document.createElement('div');
                    roomDiv.className = 'form-check';
                    roomDiv.innerHTML = `
                        <input class="form-check-input room-checkbox" type="checkbox" id="room${room.id}" data-floor-id="${floorId}" data-room-id="${room.id}">
                        <label class="form-check-label" for="room${room.id}">
                            ${room.name}
                        </label>
                    `;
                    roomsList.appendChild(roomDiv);
                });

                const roomCheckboxes = roomsList.querySelectorAll('.room-checkbox');
                roomCheckboxes.forEach(checkbox => {
                    checkbox.addEventListener('change', updateFloorStatus);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while loading rooms');
            });
    }

    function toggleAllRooms(e, floorId) {
        const isChecked = e.target.checked;
        const roomCheckboxes = document.querySelectorAll(`#roomsList${floorId} .room-checkbox`);
        roomCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        updateAllFloorsStatus();
    }

    function updateFloorStatus(e) {
        const floorId = e.target.dataset.floorId;
        const selectAllRooms = document.getElementById(`selectAllRooms${floorId}`);
        const roomCheckboxes = document.querySelectorAll(`#roomsList${floorId} .room-checkbox`);
        const allChecked = Array.from(roomCheckboxes).every(checkbox => checkbox.checked);
        const someChecked = Array.from(roomCheckboxes).some(checkbox => checkbox.checked);
        
        selectAllRooms.checked = allChecked;
        selectAllRooms.indeterminate = someChecked && !allChecked;
        
        updateAllFloorsStatus();
    }

    function updateAllFloorsStatus() {
        const allRoomsCheckboxes = document.querySelectorAll('.select-all-rooms');
        const allChecked = Array.from(allRoomsCheckboxes).every(checkbox => checkbox.checked);
        const someChecked = Array.from(allRoomsCheckboxes).some(checkbox => checkbox.checked || checkbox.indeterminate);
        
        selectAllFloors.checked = allChecked;
        selectAllFloors.indeterminate = someChecked && !allChecked;
    }

    function pauseResumeInventory(inventoryId, action) {
    showConfirmation(
        'Confirm Action',
        `Are you sure you want to ${action} this inventory?`,
        `Yes, ${action} it!`,
        'Cancel'
    ).then((result) => {
        if (result.isConfirmed) {
            fetch('{% url "api_pause_resume_inventory" %}', {
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
                fetch('{% url "api_cancel_inventory" %}', {
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

    function updateStatus(button, newStatus) {
        const row = button.closest('tr');
        const statusCell = row.querySelector('td:nth-child(4)');
        statusCell.innerHTML = getStatusBadge(newStatus);
    }

    function disableButtons(row) {
        row.querySelectorAll('.pause-resume, .end, .cancel').forEach(btn => {
            btn.disabled = true;
            btn.classList.add('disabled');
        });
    }

    function getStatusBadge(status) {
        switch (status) {
            case 'ACTIVE':
                return '<span class="badge text-success bg-light border border-success"><i class="bi bi-play-circle-fill me-1"></i>Active</span>';
            case 'PAUSED':
                return '<span class="badge bg-warning text-dark"><i class="bi bi-pause-circle-fill me-1"></i>Paused</span>';
            case 'CANCELED':
                return '<span class="badge bg-danger"><i class="bi bi-x-circle-fill me-1"></i>Canceled</span>';
            case 'COMPLETED':
                return '<span class="badge bg-success text-white"><i class="bi bi-check-circle-fill me-1"></i>Completed</span>';
            default:
                return `<span class="badge bg-secondary"><i class="bi bi-question-circle-fill me-1"></i>${status}</span>`;
        }
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
