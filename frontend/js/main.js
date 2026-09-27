// Main application initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log('Gwadar Cargo Network - Application initialized');
    
    // Initialize app based on current page
    const path = window.location.pathname;
    
    if (path.includes('/admin/')) {
        console.log('Admin Dashboard loaded');
    } else if (path.includes('/port/')) {
        console.log('Port Officer interface loaded');
    } else if (path.includes('/checkpoint/')) {
        console.log('Checkpoint interface loaded');
    } else if (path.includes('/driver/')) {
        console.log('Driver app loaded');
    }
});
