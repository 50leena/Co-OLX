// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Add loading states to buttons
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                
                // Revert after 5 seconds if still on page (form submission failed)
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }, 5000);
            }
        });
    });
    
    // Character counter for item description
    const descriptionTextarea = document.getElementById('description');
    if (descriptionTextarea) {
        const charCount = document.querySelector('.char-count');
        
        function updateCharCount() {
            const remaining = 500 - descriptionTextarea.value.length;
            charCount.textContent = `${descriptionTextarea.value.length}/500 characters`;
            
            if (remaining < 50) {
                charCount.style.color = 'var(--danger)';
            } else if (remaining < 100) {
                charCount.style.color = 'var(--warning)';
            } else {
                charCount.style.color = 'var(--text-light)';
            }
        }
        
        descriptionTextarea.addEventListener('input', updateCharCount);
        updateCharCount(); // Initial call
    }
    
    // Price input formatting
    const priceInput = document.querySelector('input[name="price"]');
    if (priceInput) {
        priceInput.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Item card hover effects
    const itemCards = document.querySelectorAll('.item-card, .listing-card');
    itemCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    this.form.submit();
                }
            }, 500);
        });
    }
});

// Marketplace sorting
function sortItems(sortBy) {
    const grid = document.getElementById('itemsGrid');
    if (!grid) return;
    
    const items = Array.from(grid.getElementsByClassName('marketplace-item'));
    
    items.sort((a, b) => {
        const priceA = parseFloat(a.dataset.price);
        const priceB = parseFloat(b.dataset.price);
        const dateA = parseFloat(a.dataset.date);
        const dateB = parseFloat(b.dataset.date);
        
        switch(sortBy) {
            case 'price_low':
                return priceA - priceB;
            case 'price_high':
                return priceB - priceA;
            case 'newest':
            default:
                return dateB - dateA;
        }
    });
    
    // Clear and re-append sorted items
    grid.innerHTML = '';
    items.forEach(item => grid.appendChild(item));
}

// Confirmation for destructive actions
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to continue?');
}

// Add to favorites functionality (placeholder)
function toggleFavorite(button) {
    button.classList.toggle('favorited');
    const icon = button.querySelector('i');
    
    if (button.classList.contains('favorited')) {
        icon.className = 'fas fa-heart';
        button.style.color = 'var(--danger)';
    } else {
        icon.className = 'far fa-heart';
        button.style.color = 'var(--text-light)';
    }
}