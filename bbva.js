// Animación para el menú de navegación
const menu = document.querySelector('nav');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 50) {
        menu.classList.add('scrolled');
    } else {
        menu.classList.remove('scrolled');
    }
});

// Animación para las secciones de la página
const sections = document.querySelectorAll('section');
window.addEventListener('scroll', () => {
    sections.forEach(section => {
        const top = section.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            section.classList.add('visible');
        }
    });
});