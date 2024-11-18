// DeviceTable.js 

// Namespace Object
let DeviceTable = {};

document.addEventListener('DOMContentLoaded', function() {

    DeviceTable.table = new DataTable('#deviceTable', {
        responsive: true,
        pageLength: 10,
        lengthMenu: [[10, 15, 20, 25], [10, 15, 20, 25]],
        dom: '<"row pb-2"<"col-12 col-lg-6 ps-lg-3 text-center text-lg-start mt-3 mb-1"li><"col-12 col-lg-6 mt-3 pe-lg-3 d-flex justify-content-center justify-content-lg-end p-0 mb-1"p>><"row"<"col-12 mx-auto"rt>><"clear">',
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
                        return '<div style="word-break: break-all; max-width: 100%">' + data + '</div>';
                    }
                    return data;
                }
            },
            { 
                width: '150px',
                targets: 2,
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; max-width: 150px;">' + data + '</div>';
                    }
                    return data;
                }
            },
            { width: '50px', targets: 4 },
            { 
                width: '100px',
                targets: 5,
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; max-width: 100px;">' + data + '</div>';
                    }
                    return data;
                }
            },
            { width: '80px', targets: 6 },
            { width: '50px', targets: 7 },
            { width: '50px', targets: 8 },
            { width: '90px', targets: 9, orderable: false }
        ]
    });

        // Search functionality
        const nameSearch = document.getElementById('nameSearch');
        const serialSearch = document.getElementById('serialSearch');
        const ownerSearch = document.getElementById('ownerSearch');
    
        function performSearch() {
            const nameValue = nameSearch.value.toLowerCase();
            const serialValue = serialSearch.value.toLowerCase();
            const ownerValue = ownerSearch.value.toLowerCase();
    
            DeviceTable.table.search('').draw(); // Clear existing search
            DeviceTable.table.columns().search('').draw(); // Clear column searches
    
            if (nameValue) DeviceTable.table.column(1).search(nameValue);
            if (serialValue) DeviceTable.table.column(2).search(serialValue);
            if (ownerValue) DeviceTable.table.column(5).search(ownerValue);
    
            DeviceTable.table.draw();
        }
    
        [nameSearch, serialSearch,ownerSearch].forEach(input => {
            input.addEventListener('keyup', performSearch);
        });
    
        // Add event listener for Apply Filters button
        document.querySelector('#filtersModal .btn-primary').addEventListener('click', function() {
            const deviceCategory = document.getElementById('deviceCategory');
            const deviceSubcategory = document.getElementById('deviceSubcategory');
            const deviceBuilding = document.getElementById('deviceBuilding');
            const deviceFloor = document.getElementById('deviceFloor');
            const deviceRoom = document.getElementById('deviceRoom');
    
            // Get selected values
            const categoryText = deviceCategory.options[deviceCategory.selectedIndex].text;
            const subcategoryText = deviceSubcategory.options[deviceSubcategory.selectedIndex].text;
            const buildingText = deviceBuilding.options[deviceBuilding.selectedIndex].text;
            const floorText = deviceFloor.options[deviceFloor.selectedIndex].text;
            const roomText = deviceRoom.options[deviceRoom.selectedIndex].text;
    
            // Clear existing column searches
            DeviceTable.table.columns().search('').draw();
    
            // Apply filters
            if (!categoryText.includes('All')) DeviceTable.table.column(3).search(categoryText);
            if (!subcategoryText.includes('All')) DeviceTable.table.column(4).search(subcategoryText);
            if (!buildingText.includes('All')) DeviceTable.table.column(6).search(buildingText);
            if (!floorText.includes('All')) DeviceTable.table.column(7).search(floorText);
            if (!roomText.includes('All')) DeviceTable.table.column(8).search(roomText);
    
            DeviceTable.table.draw();
        });

    // Category and Subcategory handling
    const deviceCategory = document.getElementById('deviceCategory');
    const deviceSubcategory = document.getElementById('deviceSubcategory');

    deviceCategory.addEventListener('change', function() {
        selectorHandler([deviceCategory, deviceSubcategory], "/get_subcategories/?category_id", ["Category", "Subcategory"], false);
    });

    // Building, Floor, and Room handling
    const deviceBuilding = document.getElementById('deviceBuilding');
    const deviceFloor = document.getElementById('deviceFloor');
    const deviceRoom = document.getElementById('deviceRoom');

    deviceBuilding.addEventListener('change', function() {
        selectorHandler([deviceBuilding, deviceFloor, deviceRoom], "/get_floors/?building_id", ["Building", "Floor", "Room"], false);
    });

    deviceFloor.addEventListener('change', function() {
        selectorHandler([deviceFloor, deviceRoom], "/get_rooms/?floor_id", ["Floor", "Room"], false);
    });

    function selectorHandler(selectors, url, modelNames, detailed_options) {
        for (var i = 1; i < selectors.length; i++) {
            if (detailed_options)
                selectors[i].innerHTML = `<option value="">Select a ${modelNames[0]} first</option>`;
            else
                selectors[i].innerHTML = `<option value="">All</option><option value="" disabled>Choose a ${modelNames[0]} first...</option>`;
        }

        let value = selectors[0].value;
        if(value){
            fetch(`${url}=${value}`)
            .then(response => response.json())
            .then(data => {
                if (!(Array.isArray(data) && data.length === 0)) {
                    if (detailed_options)
                        selectors[1].innerHTML = `<option value="">Select a ${modelNames[1]}</option>`;
                    else 
                        selectors[1].innerHTML = `<option value="">All</option>`;

                    for (var i = 2; i < selectors.length; i++) {
                        if (detailed_options) 
                            selectors[i].innerHTML = `<option value="" disabled>Please select a ${modelNames[i-1]} first.</option>`;
                        else
                            selectors[i].innerHTML = `<option value="">All</option><option value="" disabled>Choose a ${modelNames[i-1]} first...</option>`;
                    }
                    data.forEach(model => {
                        selectors[1].innerHTML += `<option value="${model.id}">${model.name}</option>`;
                    });
                } else {
                    if (detailed_options)
                        selectors[1].innerHTML = `<option value="" disabled>Please add a ${modelNames[1]} first</option>`;
                }
            })
            .catch(error => console.error('Error:', error));
        } 
    }


});
