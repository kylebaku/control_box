// static/js/theme-toggle.js
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    
    const html = document.documentElement;
    
    themeToggle.addEventListener('click', () => {
        const current = html.getAttribute('data-bs-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-bs-theme', newTheme);
        themeToggle.textContent = newTheme === 'dark' ?  '⚪' : '⚫';
        localStorage.setItem('theme', newTheme);
    });
    
    const saved = localStorage.getItem('theme');
    if (saved) {
        html.setAttribute('data-bs-theme', saved);
        themeToggle.textContent = saved === 'dark' ?  '⚪' : '⚫';
    }
});