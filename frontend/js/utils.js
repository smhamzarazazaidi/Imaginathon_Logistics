// Utility functions
const Utils = {
    formatDate(date) {
        return new Date(date).toLocaleDateString();
    },

    formatTime(date) {
        return new Date(date).toLocaleTimeString();
    },

    formatDateTime(date) {
        return new Date(date).toLocaleString();
    },

    formatCurrency(amount, currency = 'PKR') {
        return new Intl.NumberFormat('en-PK', {
            style: 'currency',
            currency
        }).format(amount);
    },

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    generateId() {
        return Math.random().toString(36).substr(2, 9);
    },

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
