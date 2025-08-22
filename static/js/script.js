// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
document.body.classList.toggle('dark-mode');
if (document.body.classList.contains('dark-mode')) {
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
} else {
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
}
});

// Chart Initialization
document.addEventListener('DOMContentLoaded', function() {
// Sales Chart
const salesCtx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Sales ($)',
            data: [125000, 150000, 175000, 140000, 195000, 230000],
            borderColor: '#2563eb',
            tension: 0.3,
            fill: true,
            backgroundColor: 'rgba(37, 99, 235, 0.1)'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Market Share Chart
const marketShareCtx = document.getElementById('marketShareChart').getContext('2d');
const marketShareChart = new Chart(marketShareCtx, {
    type: 'doughnut',
    data: {
        labels: ['Uzum', 'Ozon', 'Wildberries', 'Others'],
        datasets: [{
            data: [40, 30, 20, 10],
            backgroundColor: [
                '#2563eb',
                '#1e40af',
                '#3b82f6',
                '#93c5fd'
            ]
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Category Chart
const categoryCtx = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(categoryCtx, {
    type: 'bar',
    data: {
        labels: ['Electronics', 'Fashion', 'Home', 'Beauty', 'Food'],
        datasets: [{
            label: 'Products',
            data: [3500, 2800, 1900, 1500, 1200],
            backgroundColor: '#2563eb'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
});
