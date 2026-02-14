async function loadYouTubeVideos() {
    const container = document.querySelector('.carousel-container');
    if (!container) return;

    try {
        // Cargar el archivo JSON generado por GitHub Actions
        const response = await fetch('assets/data/videos.json');
        if (!response.ok) {
            throw new Error('No se pudo cargar la lista de videos');
        }
        const videos = await response.json();
        
        if (videos && videos.length > 0) {
            // Limpiar contenedor antes de añadir los videos
            container.innerHTML = '';

            videos.forEach(video => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'carousel-item';
                itemDiv.innerHTML = `
                    <a href="https://www.youtube.com/watch?v=${video.id}" target="_blank">
                        <img src="${video.thumbnail}" alt="${video.title}">
                        <h4>${video.title}</h4>
                    </a>
                `;
                container.appendChild(itemDiv);
            });
        }
    } catch (error) {
        console.error('Error cargando videos:', error);
        // Opcional: Mostrar mensaje de error en la UI o dejar los placeholders
    }
}

document.addEventListener('DOMContentLoaded', loadYouTubeVideos);
