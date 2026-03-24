// =====================================================
// PORTFOLIO WEBSITE - JAVASCRIPT (Flask backend)
// =====================================================

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                document.querySelector('.navbar-toggler').click();
            }
        }
    });
});

// =====================================================
// CONTACT FORM  –  posts to Flask /contact route
// =====================================================
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const name    = document.getElementById('name').value.trim();
        const email   = document.getElementById('email').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const message = document.getElementById('message').value.trim();

        clearErrorMessages();
        let isValid = true;

        if (!name)   { showError('nameError');    isValid = false; }
        if (!email)  { showError('emailError');   isValid = false; }
        else if (!isValidEmail(email)) {
            document.getElementById('emailError').textContent = 'Please enter a valid email address';
            showError('emailError'); isValid = false;
        }
        if (!subject) { showError('subjectError'); isValid = false; }
        if (!message) { showError('messageError'); isValid = false; }
        if (!isValid) return;

        // Show spinner
        const btn     = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');
        const spinner = document.getElementById('btnSpinner');
        if (btn && btnText && spinner) {
            btn.disabled = true;
            btnText.classList.add('d-none');
            spinner.classList.remove('d-none');
        }

        try {
            const formData = new FormData();
            formData.append('name',    name);
            formData.append('email',   email);
            formData.append('subject', subject);
            formData.append('message', message);

            const response = await fetch('/contact', { method: 'POST', body: formData });
            const data     = await response.json();

            if (data.success) {
                showFormMessage(data.message, 'success');
                contactForm.reset();
            } else {
                showFormMessage(data.message || 'Something went wrong. Please try again.', 'danger');
            }
        } catch (err) {
            showFormMessage('Network error. Please check your connection and try again.', 'danger');
        } finally {
            if (btn && btnText && spinner) {
                btn.disabled = false;
                btnText.classList.remove('d-none');
                spinner.classList.add('d-none');
            }
        }
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
function showError(errorId) {
    const el = document.getElementById(errorId);
    if (el) el.classList.remove('d-none');
}
function clearErrorMessages() {
    document.querySelectorAll('[id$="Error"]').forEach(el => el.classList.add('d-none'));
}
function showFormMessage(message, type) {
    const el = document.getElementById('formMessage');
    if (el) {
        el.textContent = message;
        el.className = `alert alert-${type} mt-3`;
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Real-time field validation
['name', 'email', 'subject', 'message'].forEach(field => {
    const input = document.getElementById(field);
    if (!input) return;
    input.addEventListener('blur', function () {
        const empty = this.value.trim() === '';
        const invalid = field === 'email' && !empty && !isValidEmail(this.value);
        this.classList.toggle('is-invalid', empty || invalid);
        const errEl = document.getElementById(field + 'Error');
        if (errEl) errEl.classList.toggle('d-none', !empty && !invalid);
    });
});

// Active navbar highlight on scroll
window.addEventListener('scroll', () => {
    const sections  = document.querySelectorAll('section[id]');
    const navLinks  = document.querySelectorAll('.navbar-nav .nav-link');
    let currentSection = '';
    sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - 100) currentSection = section.getAttribute('id');
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentSection) link.classList.add('active');
    });
});

// Scroll-reveal animation
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.8s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -100px 0px' });

document.querySelectorAll('.skill-card, .project-card, .education-card, .experience-card, .contact-info-card')
        .forEach(card => observer.observe(card));

// Button hover lift
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function () { this.style.transform = 'translateY(-2px)'; });
    btn.addEventListener('mouseleave', function () { this.style.transform = 'translateY(0)'; });
});

console.log('%c Welcome to Ingabire Kalinda Irene\'s Portfolio! ',
            'background:#0d6efd;color:white;font-size:14px;padding:10px;');
