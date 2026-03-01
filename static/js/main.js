// ─── Mobile Navigation Toggle ─────────────
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('mobileToggle');
    const links = document.getElementById('navbarLinks');

    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('open');
            const icon = toggle.querySelector('i');
            icon.classList.toggle('bi-list');
            icon.classList.toggle('bi-x');
        });

        // Close menu on link click
        links.querySelectorAll('a, button').forEach(el => {
            el.addEventListener('click', () => {
                links.classList.remove('open');
                const icon = toggle.querySelector('i');
                icon.classList.add('bi-list');
                icon.classList.remove('bi-x');
            });
        });
    }

    // ─── Auto-dismiss alerts ──────────────
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });

    // ─── Star Rating ──────────────────────
    const starLabels = document.querySelectorAll('.star-rating label');
    const ratingInput = document.getElementById('id_rating');

    starLabels.forEach(label => {
        label.addEventListener('click', () => {
            const value = label.getAttribute('data-value');
            if (ratingInput) {
                ratingInput.value = value;
            }
        });
    });
});
