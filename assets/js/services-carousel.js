document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    const slidesContainer = document.querySelector('.services-slides');
    const slides = document.querySelectorAll('.service-slide');
    const totalSlides = slides.length;
    const dots = document.querySelectorAll('.dot');

    if (!slidesContainer || slides.length === 0) return;

    function showSlide(index) {
        // Asegurar que el índice esté dentro de los límites
        if (index >= totalSlides) {
            slideIndex = 0;
        } else if (index < 0) {
            slideIndex = totalSlides - 1;
        } else {
            slideIndex = index;
        }
        
        // Calcular el porcentaje de desplazamiento lateral
        const percent = -(slideIndex * 100);
        slidesContainer.style.transform = `translateX(${percent}%)`;
        
        // Actualizar estado de los puntos
        dots.forEach(dot => dot.classList.remove('active'));
        if (dots[slideIndex]) {
            dots[slideIndex].classList.add('active');
        }
    }

    // Exponer la función currentSlide globalmente para que funcione con onclick en HTML
    window.currentSlide = function(n) {
        // n viene como 1-based desde el HTML
        showSlide(n - 1);
    };

    // Inicializar el carrusel
    showSlide(slideIndex);

    // Opcional: Auto-play cada 5 segundos
    setInterval(() => {
        showSlide(slideIndex + 1);
    }, 5000);
});