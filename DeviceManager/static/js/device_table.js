// DeviceTable.js 

// Namespace Object
let DeviceTable = {};

document.addEventListener('DOMContentLoaded', function() {

    DeviceTable.table = new DataTable('#deviceTable', {
        responsive: true,
        pageLength: 5,
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        dom: '<"row pb-2"<"col-12 col-lg-6 text-center text-lg-start mb-1"li><"col-12 col-lg-6 d-flex justify-content-center justify-content-lg-end p-0 mb-1"p>><"row"<"col-12"rt>><"clear">',
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
            { width: '40px', targets: 0 },
            { 
                width: '100%',
                targets: 1,
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; min-width: 100px;">' + data + '</div>';
                    }
                    return data;
                }

            },   // ID
            { 
                width: '100%',
                targets: 2, // Assuming S/N is the 3rd column (index 2)
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; min-width: 120px;">' + data + '</div>';
                    }
                    return data;
                }
            },
            { width: '50px',targets: 4 },
            { 
                width: '100px',
                targets:5,
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; max-width: 100px;">' + data + '</div>';
                    }
                    return data;
                }
            },
            { width: '80px', targets:6 },
            { width: '50px', targets: 7 },  // S/N
            { width: '50px',targets: 8},
            { width: '120px',targets: 9, orderable: false},
        ],
        initComplete: function (settings, json) {
            
            this.api().columns().every(function (index) {
                let column = this;
                    let input = document.querySelector('.search-row th:nth-child(' + (index + 1) + ') input');                
                if (input) {
                    input.addEventListener('keyup', () => {
                        if (column.search() !== input.value) {
                            column.search(input.value).draw();
                        }
                    });
                }
            });
        }
    });

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

    // Category and Subcategory handling
    const deviceCategory = document.getElementById('deviceCategory');
    const deviceSubcategory = document.getElementById('deviceSubcategory');
    
    deviceCategory.addEventListener('change', function() {
        selectorHandler([deviceCategory, deviceSubcategory], "/get_subcategories/?category_id", ["Category", "Subcategory"], false);
        
        let selectedOption = this.options[this.selectedIndex];
        let selectedText = selectedOption ? selectedOption.textContent : '';
        
        if(selectedText === 'All') {
            DeviceTable.table.column(4).search('').draw();
            DeviceTable.table.column(3).search('').draw();
        } else {
            DeviceTable.table.column(3).search(selectedText).draw();
        }
    });
    deviceSubcategory.addEventListener('change', function() {
        let selectedOption = this.options[this.selectedIndex];
        let selectedText = selectedOption ? selectedOption.textContent : '';
        
        if(selectedText === 'All') {
            DeviceTable.table.column(4).search('').draw();
        } else {
            DeviceTable.table.column(4).search(selectedText).draw();
        }
    });

    // Building, Floor, and Room handling
    const deviceBuilding = document.getElementById('deviceBuilding');
    const deviceFloor = document.getElementById('deviceFloor');
    const deviceRoom = document.getElementById('deviceRoom');

    deviceBuilding.addEventListener('change', function() {
        selectorHandler([deviceBuilding, deviceFloor, deviceRoom], "/get_floors/?building_id", ["Building", "Floor", "Room"], false);


        let selectedOption = this.options[this.selectedIndex];
        let selectedText = selectedOption ? selectedOption.textContent : '';
        
        if(selectedText === 'All') {
            DeviceTable.table.column(8).search('').draw();
            DeviceTable.table.column(7).search('').draw();
            DeviceTable.table.column(6).search('').draw();
        } else {
            DeviceTable.table.column(6).search(selectedText).draw();
        }
    });
    deviceFloor.addEventListener('change', function() {
        selectorHandler([deviceFloor, deviceRoom], "/get_rooms/?floor_id", ["Floor", "Room"], false);
        
        let selectedOption = this.options[this.selectedIndex];
        let selectedText = selectedOption ? selectedOption.textContent : '';
        
        if(selectedText === 'All') {
            DeviceTable.table.column(8).search('').draw();
            DeviceTable.table.column(7).search('').draw();
        } else {
            DeviceTable.table.column(7).search(selectedText).draw();
        }
    });
    deviceRoom.addEventListener('change', function() {
        let selectedOption = this.options[this.selectedIndex];
        let selectedText = selectedOption ? selectedOption.textContent : '';
        
        if(selectedText === 'All') {
            DeviceTable.table.column(8).search('').draw();
        } else {
            DeviceTable.table.column(8).search(selectedText).draw();
        }
    });


});

function hideColumns(table, columnsToHide) {
    columnsToHide.forEach(columnIdx => {
        let column = table.column(columnIdx);
        column.visible(!column.visible());
    });
}