// ========================================
// Kagai - Love Notes App
// Main JavaScript Functionality
// ========================================

// Initialize event listeners on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFormValidation();
    initializeCharCounters();
});

// ============ Tooltips ============
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ============ Form Validation ============
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// ============ Character Counters ============
function initializeCharCounters() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(textarea => {
        const updateCounter = () => {
            const remaining = textarea.maxLength - textarea.value.length;
            const percentage = (textarea.value.length / textarea.maxLength) * 100;
            
            if (percentage > 90) {
                textarea.classList.add('is-warning');
            } else {
                textarea.classList.remove('is-warning');
            }
        };
        
        textarea.addEventListener('input', updateCounter);
    });
}

// ============ Search & Filter ============
function filterUsers(query) {
    const userCards = document.querySelectorAll('.user-card');
    const lowerQuery = query.toLowerCase();
    
    userCards.forEach(card => {
        const username = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const location = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
        
        if (username.includes(lowerQuery) || location.includes(lowerQuery)) {
            card.parentElement.style.display = '';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}

// ============ Favorite Toggle ============
function toggleFavorite(noteId) {
    const button = event.target.closest('button');
    const url = `/note/favorite/${noteId}/`;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.favorited) {
            button.classList.remove('btn-outline-danger');
            button.classList.add('btn-danger');
            button.innerHTML = '<i class="fas fa-star"></i> Favorited';
            showNotification('Added to favorites!', 'success');
        } else {
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-danger');
            button.innerHTML = '<i class="fas fa-star"></i> Add to Favorites';
            showNotification('Removed from favorites', 'info');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Something went wrong', 'error');
    });
}

// ============ Notifications ============
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// ============ Image Preview ============
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const preview = document.querySelector('.avatar-preview');
            if (preview) {
                preview.src = e.target.result;
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// ============ Copy to Clipboard ============
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

// ============ Smooth Scroll ============
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ============ Search with Debounce ============
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function(e) {
        filterUsers(e.target.value);
    }, 300));
}

// ============ Lazy Loading Images ============
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
}

// ============ Performance Metrics ============
if (window.performance && window.performance.timing) {
    window.addEventListener('load', function() {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log('Page load time: ' + pageLoadTime + ' ms');
    });
}

// ============ Service Worker Registration (Optional) ============
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/sw.js').catch(() => {
        // Service worker not available
    });
}

// ============ Export Functions ============
window.Kagai = {
    toggleFavorite,
    filterUsers,
    copyToClipboard,
    showNotification,
    previewImage
};
