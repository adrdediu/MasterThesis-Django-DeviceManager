document.addEventListener('DOMContentLoaded', function() {
    // View switching
    const listViewBtn = document.getElementById('listViewBtn');
    const cardViewBtn = document.getElementById('cardViewBtn');
    const listViewContainer = document.getElementById('listViewContainer');
    const cardViewContainer = document.getElementById('cardViewContainer');
    const cardPagination = document.getElementById('cardPagination');

    // Load saved view preference
    const savedView = localStorage.getItem(`viewPreference_${window.location.pathname}`);
    if (savedView === 'card') {
        listViewContainer.style.display = 'none';
        cardViewContainer.style.display = 'block';
        cardViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
        updateCardView();
    } 

    listViewBtn.addEventListener('click', function() {
        listViewContainer.style.display = 'block';
        cardViewContainer.style.display = 'none';
        cardPagination.style.display = 'none';
        listViewBtn.classList.add('active');
        cardViewBtn.classList.remove('active');
        localStorage.setItem(`viewPreference_${window.location.pathname}`, 'list');
         // Redraw the DataTable
        DeviceTable.table.columns.adjust().draw();
    });

    cardViewBtn.addEventListener('click', function() {
        listViewContainer.style.display = 'none';
        cardViewContainer.style.display = 'block';
        cardPagination.style.display = 'block';
        cardViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
        localStorage.setItem(`viewPreference_${window.location.pathname}`, 'card');
        updateCardView();
    });

    // Load saved filter values
    //loadFilterValues();
    updateFilterButton();

    setTimeout(function() {
        document.getElementById('skeletonLoader').style.display = 'none';
        document.getElementById('deviceListContent').style.display = 'block';
        if(savedView !== 'card') {
            DeviceTable.table.columns.adjust().draw();
        }
    }, 500);
});


function loadFilterValues() {
    const inputs = ['nameSearch', 'serialSearch', 'ownerSearch'];
    const selects = ['deviceCategory', 'deviceSubcategory', 'deviceBuilding', 'deviceFloor', 'deviceRoom'];

    inputs.forEach(id => {
        const element = document.getElementById(id);
        const savedValue = sessionStorage.getItem(id);
        if (savedValue) element.value = savedValue;
    });

    selects.forEach(id => {
        const element = document.getElementById(id);
        const savedValue = sessionStorage.getItem(id);
        if (savedValue) element.value = savedValue;
    });
}

function updateFilterButton() {
    const filterBtn = document.querySelector('[data-bs-target="#filtersModal"]');
    
    const hasFilters = ['deviceCategory', 'deviceSubcategory', 'deviceBuilding', 'deviceFloor', 'deviceRoom']
        .some(id => {
            const element = document.getElementById(id);
            return element.value && element.options[element.selectedIndex].text !== 'All Categories' 
                && element.options[element.selectedIndex].text !== 'All Subcategories'
                && element.options[element.selectedIndex].text !== 'All Buildings'
                && element.options[element.selectedIndex].text !== 'All Floors'
                && element.options[element.selectedIndex].text !== 'All Rooms';
        });

    filterBtn.innerHTML = `
        <i class="bi bi-filter${hasFilters ? '-circle' : ''}"></i>
        Filter${hasFilters ? 'ed' : 's'}
    `;

    filterBtn.classList.toggle('btn-success', hasFilters);
    filterBtn.classList.toggle('btn-dark', !hasFilters);
    
}
