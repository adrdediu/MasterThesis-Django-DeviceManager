document.addEventListener('DOMContentLoaded', function() {
    const changeToIoTUIBtn = document.getElementById('changeToIoTUI');
    const changeToGeneralInfoBtn = document.getElementById('changeToGeneralInfo');
    const setUIBtns = document.querySelectorAll('.set-default-ui');
    const currentUILabel = document.getElementById('currentUILabel');
    const generalInfoCard = document.getElementById('generalInfoCard');
    const iotUICard = document.getElementById('iotUICard');
    const skeletonLoader = document.getElementById('skeletonLoader');
    const deviceId = document.getElementById('device-id').dataset.deviceId;

    let currentUI = localStorage.getItem(`device_${deviceId}_defaultUI`) || 'general';
    updateUIDisplay();

    changeToIoTUIBtn.addEventListener('click', () => toggleUI('iot'));
    changeToGeneralInfoBtn.addEventListener('click', () => toggleUI('general'));
    setUIBtns.forEach(btn => btn.addEventListener('click', setDefaultUI));

    function toggleUI(newUI) {
        currentUI = newUI;
        updateUIDisplay(true);
    }

    function updateUIDisplay(immediate = false) {
        if (immediate) {
            showCurrentUI();
        } else {
            skeletonLoader.style.display = 'block';
            generalInfoCard.style.display = 'none';
            iotUICard.style.display = 'none';
    
            setTimeout(() => {
                skeletonLoader.style.display = 'none';
                showCurrentUI();
            }, 800); // Simulate loading time
        }
    }
    
    function showCurrentUI() {
        if (currentUI === 'general') {
            generalInfoCard.style.display = 'block';
            iotUICard.style.display = 'none';
            changeToIoTUIBtn.style.display = 'inline-block';
            changeToGeneralInfoBtn.style.display = 'none';
        } else {
            generalInfoCard.style.display = 'none';
            iotUICard.style.display = 'block';
            changeToIoTUIBtn.style.display = 'none';
            changeToGeneralInfoBtn.style.display = 'inline-block';
        }
        currentUILabel.textContent = currentUI === 'general' ? 'General Information' : 'IoT UI';
    }
    

    function setDefaultUI() {
        localStorage.setItem(`device_${deviceId}_defaultUI`, currentUI);
        showAlert('Default UI set successfully', 'success');
    }
    

    
});
