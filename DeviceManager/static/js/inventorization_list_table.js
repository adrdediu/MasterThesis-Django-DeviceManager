// Inventorization_List_Table.js 

// Namespace Object
let InventorizationListsTable = {};

document.addEventListener('DOMContentLoaded', function() {

    // Initialize DataTable
    InventorizationListsTable.table = new DataTable('#inventorizationTable', {
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
            { 
                width: '170px',
                targets: 1,
                render: function(data, type, row) {
                    if (type === 'display') {
                        return '<div style="word-break: break-all; max-width: 170px;">' + data + '</div>';
                    }
                    return data;
                }
            },  // Name
            { width: '110px', targets: 4 },  // Description
            { width: '110px', targets: 5 },  // Location
            { width: '150px',  targets: 6, orderable: false }  // Actions
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
});