/**
 * Food Waste Tracker - Main JavaScript File
 * All client-side functionality centralized in this file
 */

// Wait for DOM to be fully loaded before executing scripts
document.addEventListener('DOMContentLoaded', function() {
    initializeFoodTracking();
    initializeFormHandlers();
    initializeDashboardFeatures();
    initializeDonationFeatures();
    initializeDateValidation();
    initializeDonationSearch();
    initializeExpiryColorCoding();
});

/**
 * Food Tracking Functionality
 * Handles marking food as consumed/wasted and status updates
 */
function initializeFoodTracking() {
    // Add event listeners to all food status buttons
    document.querySelectorAll('.mark-consumed').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            updateFoodStatus(itemId, 'consumed');
        });
    });
    
    document.querySelectorAll('.mark-wasted').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            updateFoodStatus(itemId, 'wasted');
        });
    });
}

/**
 * Update food item status via AJAX
 * @param {string} itemId - ID of the food item
 * @param {string} status - New status ('consumed' or 'wasted')
 */
function updateFoodStatus(itemId, status) {
    if (!confirm(`Are you sure you want to mark this item as ${status}?`)) {
        return;
    }
    
    showLoadingState(true);
    
    fetch(`/food/update_status/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({status: status})
    })
    .then(response => response.json())
    .then(data => {
        showLoadingState(false);
        
        if (data.success) {
            showAlert('Status updated successfully!', 'success');
            // Reload page after short delay to show updated state
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('Error updating status', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showLoadingState(false);
        showAlert('Network error occurred', 'error');
    });
}

/**
 * Form Handling and Validation
 */
function initializeFormHandlers() {
    // Add real-time validation to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Please fill in all required fields correctly', 'error');
            }
        });
        
        // Add input validation on field blur
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

/**
 * Date validation for food forms
 */
function initializeDateValidation() {
    const expiryDateFields = document.querySelectorAll('input[type="date"]');
    const foodForm = document.getElementById('add-food-form');
    
    if (foodForm) {
        // Set minimum date for expiry date to today
        const expiryDateField = document.getElementById('expiry_date');
        if (expiryDateField) {
            const today = new Date().toISOString().split('T')[0];
            expiryDateField.min = today;
        }
        
        // Custom validation for expiry date
        foodForm.addEventListener('submit', function(e) {
            const expiryDate = new Date(expiryDateField.value);
            const purchaseDateField = document.getElementById('purchase_date');
            const purchaseDate = new Date(purchaseDateField.value || today);
            
            if (expiryDate < purchaseDate) {
                e.preventDefault();
                showAlert('❌ Expiry date cannot be before purchase date!', 'error');
                expiryDateField.focus();
            }
        });
    }
}

/**
 * Validate entire form before submission
 * @param {HTMLFormElement} form - Form element to validate
 * @returns {boolean} - True if form is valid
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate individual form field
 * @param {HTMLElement} field - Input field to validate
 * @returns {boolean} - True if field is valid
 */
function validateField(field) {
    const value = field.value.trim();
    const isValid = value !== '';
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

/**
 * Dashboard Features and Analytics
 */
function initializeDashboardFeatures() {
    // Initialize any charts if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        initializeWasteCharts();
    }
}

/**
 * Initialize waste analytics charts
 */
function initializeWasteCharts() {
    // Check if chart containers exist
    const wasteChartEl = document.getElementById('waste-chart');
    const categoryChartEl = document.getElementById('category-chart');
    
    if (wasteChartEl) {
        fetchWasteTrendData();
    }
    
    if (categoryChartEl) {
        fetchCategoryBreakdownData();
    }
}

/**
 * Fetch waste trend data and render chart
 */
function fetchWasteTrendData() {
    fetch('/analytics/api/waste_trend')
        .then(response => response.json())
        .then(data => {
            renderWasteTrendChart(data);
        })
        .catch(error => {
            console.error('Error fetching waste trend data:', error);
        });
}

/**
 * Fetch category breakdown data and render chart
 */
function fetchCategoryBreakdownData() {
    fetch('/analytics/api/category_breakdown')
        .then(response => response.json())
        .then(data => {
            renderCategoryBreakdownChart(data);
        })
        .catch(error => {
            console.error('Error fetching category data:', error);
        });
}

/**
 * Render waste trend line chart
 * @param {Object} data - Chart data from API
 */
function renderWasteTrendChart(data) {
    const ctx = document.getElementById('waste-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.months,
            datasets: [
                {
                    label: 'Consumed',
                    data: data.consumed,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Wasted',
                    data: data.wasted,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Consumption vs Waste'
                }
            }
        }
    });
}

/**
 * Render category breakdown bar chart
 * @param {Object} data - Chart data from API
 */
function renderCategoryBreakdownChart(data) {
    const ctx = document.getElementById('category-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.category),
            datasets: [{
                label: 'Waste Percentage',
                data: data.map(item => item.waste_percentage),
                backgroundColor: data.map((item, index) => 
                    `hsl(${index * 30}, 70%, 60%)`
                )
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Waste Percentage (%)'
                    },
                    max: 100
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Waste by Food Category'
                }
            }
        }
    });
}

/**
 * Donation System Features
 */
function initializeDonationFeatures() {
    // Add claim donation handlers
    document.querySelectorAll('.claim-donation').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const donationId = this.dataset.id;
            claimDonation(donationId);
        });
    });
}

/**
 * Claim a donation via AJAX
 * @param {string} donationId - ID of the donation to claim
 */
function claimDonation(donationId) {
    if (!confirm('Are you sure you want to claim this donation?')) {
        return;
    }
    
    showLoadingState(true);
    
    fetch(`/donations/claim/${donationId}`, {
        method: 'POST'
    })
    .then(response => {
        showLoadingState(false);
        if (response.ok) {
            showAlert('Donation claimed successfully!', 'success');
            setTimeout(() => {
                window.location.href = '/donations/my_claims';
            }, 1500);
        } else {
            showAlert('Error claiming donation', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showLoadingState(false);
        showAlert('Network error occurred', 'error');
    });
}

/**
 * Donation search functionality
 */
function initializeDonationSearch() {
    const searchInput = document.getElementById('donation-search');
    const categoryFilter = document.getElementById('category-filter');
    
    if (searchInput || categoryFilter) {
        const filterDonations = () => {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const categoryTerm = categoryFilter ? categoryFilter.value : '';
            const donationItems = document.querySelectorAll('.donation-item');
            
            donationItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                const category = item.querySelector('.badge.bg-secondary')?.textContent || '';
                
                const matchesSearch = text.includes(searchTerm);
                const matchesCategory = !categoryTerm || category.includes(categoryTerm);
                
                if (matchesSearch && matchesCategory) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        };
        
        if (searchInput) {
            searchInput.addEventListener('input', filterDonations);
        }
        if (categoryFilter) {
            categoryFilter.addEventListener('change', filterDonations);
        }
    }
}

/**
 * Initialize expiry warning color coding
 */
function initializeExpiryColorCoding() {
    document.querySelectorAll('.expiry-warning').forEach(element => {
        const days = parseInt(element.dataset.days);
        colorCodeExpiryWarning(element, days);
    });
}

/**
 * Color code expiry warnings based on days remaining
 * @param {HTMLElement} element - Element to color code
 * @param {number} days - Days until expiry
 */
function colorCodeExpiryWarning(element, days) {
    // Remove existing color classes
    element.classList.remove('expiry-critical', 'expiry-warning', 'expiry-caution', 'expiry-good');
    
    if (days <= 0) {
        element.classList.add('expiry-critical');
    } else if (days <= 2) {
        element.classList.add('expiry-warning');
    } else if (days <= 5) {
        element.classList.add('expiry-caution');
    } else {
        element.classList.add('expiry-good');
    }
}

/**
 * Utility Functions
 */

/**
 * Show alert message to user
 * @param {string} message - Message to display
 * @param {string} type - Alert type: 'success', 'error', 'warning', 'info'
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    const alertClass = `alert alert-${type === 'error' ? 'danger' : type}`;
    
    alertDiv.className = `${alertClass} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to the top of the content container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

/**
 * Show/hide loading state
 * @param {boolean} isLoading - Whether to show loading state
 */
function showLoadingState(isLoading) {
    if (isLoading) {
        document.body.style.cursor = 'wait';
        // You could add a global loading spinner here
    } else {
        document.body.style.cursor = 'default';
    }
}

/**
 * Generic API call function
 * @param {string} url - API endpoint URL
 * @param {string} method - HTTP method (GET, POST, etc.)
 * @param {Object} data - Request data
 * @returns {Promise} - Fetch promise
 */
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}