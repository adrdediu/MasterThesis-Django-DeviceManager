let currentPage = 1;
let pageSize = 12;

function updateCardView() {
    const cards = document.querySelectorAll('#cardViewContainer .col');
    const totalPages = Math.ceil(cards.length / pageSize);
    
    // Hide all cards first
    cards.forEach(card => card.style.display = 'none');
    
    // Show cards for current page
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    
    for(let i = start; i < end && i < cards.length; i++) {
        cards[i].style.display = 'block';
    }
    
    // Update pagination UI
    updatePaginationControls(totalPages);
}

function updatePaginationControls(totalPages) {
    const paginationHTML = `
        <div class="d-flex align-items-center float-end">
            <select class="form-select form-select-sm me-2" id="pageSizeSelect" style="width: auto;">
                <option value="4">4</option>
                <option value="8">8</option>
                <option value="12">12</option>
                <option value="24">24</option>
                <option value="36">36</option>
                <option value="48">48</option>
            </select>
            <ul class="pagination pagination-sm mb-0">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="first">&laquo;</a>
                </li>
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="prev">&lt;</a>
                </li>
                <li class="page-item active">
                    <span class="page-link">${currentPage} of ${totalPages}</span>
                </li>
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="next">&gt;</a>
                </li>
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="last">&raquo;</a>
                </li>
            </ul>
        </div>
    `;
    
    const paginationContainer = document.getElementById('cardPagination');
    paginationContainer.innerHTML = paginationHTML;
    
    // Page size select handler
    document.getElementById('pageSizeSelect').value = pageSize;
    document.getElementById('pageSizeSelect').addEventListener('change', (e) => {
        pageSize = parseInt(e.target.value);
        currentPage = 1;
        updateCardView();
    });

    // Pagination controls handlers
    paginationContainer.querySelectorAll('.page-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const action = e.target.dataset.page;
            
            switch(action) {
                case 'first':
                    currentPage = 1;
                    break;
                case 'last':
                    currentPage = totalPages;
                    break;
                case 'prev':
                    if(currentPage > 1) currentPage--;
                    break;
                case 'next':
                    if(currentPage < totalPages) currentPage++;
                    break;
            }
            
            updateCardView();
        });
    });
}
function filterCards() {
    // Reset to first page when filtering
    currentPage = 1;
    
    const nameFilter = document.getElementById('nameSearch').value.toLowerCase();
    const serialFilter = document.getElementById('serialSearch').value.toLowerCase();
    const ownerFilter = document.getElementById('ownerSearch').value.toLowerCase();
    const categoryFilter = document.getElementById('deviceCategory').options[document.getElementById('deviceCategory').selectedIndex].text;
    const subcategoryFilter = document.getElementById('deviceSubcategory').options[document.getElementById('deviceSubcategory').selectedIndex].text;
    const buildingFilter = document.getElementById('deviceBuilding').options[document.getElementById('deviceBuilding').selectedIndex].text;
    const floorFilter = document.getElementById('deviceFloor').options[document.getElementById('deviceFloor').selectedIndex].text;
    const roomFilter = document.getElementById('deviceRoom').options[document.getElementById('deviceRoom').selectedIndex].text;
    
    // Save filter values to sessionStorage
    sessionStorage.setItem('nameSearch', nameFilter);
    sessionStorage.setItem('serialSearch', serialFilter);
    sessionStorage.setItem('ownerSearch', ownerFilter);
    sessionStorage.setItem('deviceCategory', categoryFilter.value);
    sessionStorage.setItem('deviceSubcategory', subcategoryFilter.value);
    sessionStorage.setItem('deviceBuilding', buildingFilter.value);
    sessionStorage.setItem('deviceFloor', floorFilter.value);
    sessionStorage.setItem('deviceRoom', roomFilter.value);


    const cards = document.querySelectorAll('#cardViewContainer .col');
    
    cards.forEach(card => {
        const name = card.querySelector('.card-title').textContent.toLowerCase();
        const serial = card.querySelector('[data-serial]').textContent.toLowerCase();
        const owner = card.querySelector('.text-muted').textContent.toLowerCase();
        const category = card.querySelector('[data-category]').textContent;
        const subcategory = card.querySelector('[data-subcategory]').textContent;
        const building = card.querySelector('[data-building]').textContent;
        const floor = card.querySelector('[data-floor]').textContent;
        const room = card.querySelector('[data-room]').textContent;

        console.log(category,categoryFilter,categoryFilter === category)
        const matchesFilters = 
        (nameFilter === '' || name.includes(nameFilter)) &&
        (serialFilter === '' || serial.includes(serialFilter)) &&
        (ownerFilter === '' || owner.includes(ownerFilter)) &&
        (categoryFilter.includes('All') || category === categoryFilter) &&
        (subcategoryFilter.includes('All') || subcategory === subcategoryFilter) &&
        (buildingFilter.includes('All') || building === buildingFilter) &&
        (floorFilter.includes('All') || floor === floorFilter) &&
        (roomFilter.includes('All') || room === roomFilter);
    
        console.log(matchesFilters)
        card.classList.toggle('d-none', !matchesFilters);
    });

    updateFilterButton();
    updateCardView();
}

// Initialize card view when switching to card view
document.getElementById('cardViewBtn').addEventListener('click', updateCardView);

// Add event listeners for filters
document.querySelectorAll('#nameSearch, #serialSearch, #ownerSearch').forEach(input => {
    input.addEventListener('keyup', filterCards);
});


// Update the Apply Filters button handler
document.querySelector('#filtersModal .btn-primary').addEventListener('click', filterCards);
