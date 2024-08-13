
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
function showConfirmation(title, text, confirmButtonText, cancelButtonText,icon='warning') {
    return Swal.fire({
        title: title,
        text: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: confirmButtonText,
        cancelButtonText: cancelButtonText
    });
}
function showAlertAndReload(message, type = 'info', delay = 2000) {
    const iconTypes = {
        success: 'success',
        warning: 'warning',
        error: 'error',
        info: 'info'
    };

    const buttonColors = {
        success: '#198754', // Bootstrap 5 success color
        warning: '#ffc107', // Bootstrap 5 warning color
        error: '#dc3545',   // Bootstrap 5 danger color
        info: '#0dcaf0'     // Bootstrap 5 info color
    };

    Swal.fire({
        title: type.charAt(0).toUpperCase() + type.slice(1),
        text: message,
        icon: iconTypes[type] || 'info',
        position: 'center',
        showConfirmButton: false,
        timer: delay,
        timerProgressBar: true
    }).then(() => {
        location.reload();
});
}
function showAlert(message, type = 'info') {
    const iconTypes = {
        success: 'success',
        warning: 'warning',
        error: 'error',
        info: 'info'
    };
    const buttonColors = {
        success: '#198754', // Bootstrap 5 success color
        warning: '#ffc107', // Bootstrap 5 warning color
        error: '#dc3545',   // Bootstrap 5 danger color
        info: '#0dcaf0'     // Bootstrap 5 info color
    };

    Swal.fire({
        title: type.charAt(0).toUpperCase() + type.slice(1),
        text: message,
        icon: iconTypes[type] || 'info',
        toast: true,
        position: 'center',
        showConfirmButton: true,
        confirmButtonText: 'OK',
        confirmButtonColor: buttonColors[type] || buttonColors.info,
    });
}


document.addEventListener('DOMContentLoaded', function() {
const profileForm = document.getElementById('profileUpdateForm');
const updateProfileBtn = document.getElementById('updateProfileBtn');
const resetProfileBtn = document.getElementById('resetProfileBtn');

updateProfileBtn.addEventListener('click', function(e) {
e.preventDefault();
if (validateForm()) {
  submitForm();
}
});

resetProfileBtn.addEventListener('click', function() {
// Reset form fields to their original values
document.getElementById('email').value = "{{ user.email }}";
document.getElementById('first_name').value = "{{ user.first_name }}";
document.getElementById('last_name').value = "{{ user.last_name }}";
document.getElementById('rank').value = "{{ user.extended_user.rank }}";
document.getElementById('faculty').value = "{{ user.extended_user.faculty }}";
document.getElementById('admin_rank').value = "{{ user.extended_user.admin_rank }}";


// Clear the password field
document.getElementById('password').value = "";

// Clear any error messages
const errorMessages = profileForm.querySelectorAll('.error-message');
errorMessages.forEach(error => error.remove());

// Remove 'is-invalid' class from all inputs
const inputs = profileForm.querySelectorAll('.form-control');
inputs.forEach(input => input.classList.remove('is-invalid'));
});

function validateForm() {
let isValid = true;

// Email validation
const emailInput = document.getElementById('email');
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(emailInput.value)) {
  showError(emailInput, 'Please enter a valid email address');
  isValid = false;
} else {
  clearError(emailInput);
}

// Name validation
const firstNameInput = document.getElementById('first_name');
const lastNameInput = document.getElementById('last_name');
if (firstNameInput.value.trim() === '') {
  showError(firstNameInput, 'First name is required');
  isValid = false;
} else {
  clearError(firstNameInput);
}
if (lastNameInput.value.trim() === '') {
  showError(lastNameInput, 'Last name is required');
  isValid = false;
} else {
  clearError(lastNameInput);
}

// Password validation
const passwordInput = document.getElementById('password');
if (passwordInput.value.trim() === '') {
  showError(passwordInput, 'Password is required to confirm changes');
  isValid = false;
} else {
  clearError(passwordInput);
}

return isValid;
}

function showError(input, message) {
const formGroup = input.closest('.mb-3');
const errorElement = formGroup.querySelector('.error-message') || document.createElement('div');
errorElement.className = 'error-message text-danger mt-1';
errorElement.textContent = message;
if (!formGroup.querySelector('.error-message')) {
  formGroup.appendChild(errorElement);
}
input.classList.add('is-invalid');
}

function clearError(input) {
const formGroup = input.closest('.mb-3');
const errorElement = formGroup.querySelector('.error-message');
if (errorElement) {
  errorElement.remove();
}
input.classList.remove('is-invalid');
}

function submitForm() {
const formData = new FormData(profileForm);
console.log("Form data entries:", Array.from(formData.entries()));
fetch('/update_profile/', {
  method: 'POST',
  body: formData,
  headers: {
    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
  }
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    bootstrap.Modal.getInstance(document.getElementById('profileInfoModal')).hide();
    showAlertAndReload ('Profile updated successfully','success');
  } else {
    showAlert(data.message,'danger');
  }
})
.catch(error => {
  console.error('Error:', error);
  showAlert('An error occurred while updating the profile','danger');
});
}
});
document.addEventListener('DOMContentLoaded', function() {
  const changePasswordBtn = document.getElementById('changePasswordBtn');
  const passwordChangeForm = document.getElementById('passwordChangeForm');

  changePasswordBtn.addEventListener('click', function() {
    if (passwordChangeForm.checkValidity()) {
      const formData = new FormData(passwordChangeForm);
      
      fetch('/change_password/', {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          bootstrap.Modal.getInstance(document.getElementById('passwordChangeModal')).hide();
          showAlert('Password changed successfully','success' );
          passwordChangeForm.reset();
        } else {
          
          showAlert( data.message,'danger');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showAlert( 'An error occurred while changing the password','danger');
      });
    } else {
      passwordChangeForm.reportValidity();
    }
  });
});
