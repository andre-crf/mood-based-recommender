// Mood-Based Recommender - Client com IMAGENS E LINKS

class MoodRecommenderWithMedia {
    constructor() {
        this.moodButtons = document.querySelectorAll('.mood-btn');
        this.resultsSection = document.getElementById('results');
        this.moodSelector = document.querySelector('.mood-selector');
        this.loadingSection = document.getElementById('loading');
        this.backBtn = document.getElementById('backBtn');
        
        this.init();
    }
    
    init() {
        this.moodButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const mood = btn.dataset.mood;
                this.handleMoodSelection(mood);
            });
        });
        
        this.backBtn.addEventListener('click', () => {
            this.showMoodSelector();
        });
    }
    
    async handleMoodSelection(mood) {
        this.showLoading();
        
        try {
            const response = await fetch('/api/recomendar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mood: mood,
                    tipo: 'tudo'
                })
            });
            
            if (!response.ok) {
                throw new Error('Erro ao buscar recomendações');
            }
            
            const data = await response.json();
            this.displayResults(data, mood);
            
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao buscar as recomendações. Tente novamente.');
            this.showMoodSelector();
        }
    }
    
    displayResults(data, mood) {
        const moodEmojis = {
            'feliz': '😄',
            'triste': '😔',
            'relaxado': '😴',
            'energizado': '😡',
            'ansioso': '😰',
            'pensativo': '🤔'
        };
        
        const moodNames = {
            'feliz': 'Feliz',
            'triste': 'Triste',
            'relaxado': 'Relaxado',
            'energizado': 'Energizado',
            'ansioso': 'Ansioso',
            'pensativo': 'Pensativo'
        };
        
        document.getElementById('selectedMood').innerHTML = 
            `${moodEmojis[mood]} ${moodNames[mood]}`;
        
        // Renderiza com imagens e links
        this.renderContentWithMedia(data.musicas, 'musicResults', 'musica');
        this.renderContentWithMedia(data.filmes, 'movieResults', 'filme');
        this.renderContentWithMedia(data.jogos, 'gameResults', 'jogo');
        
        this.showResults();
    }
    
    renderContentWithMedia(items, containerId, tipo) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        if (items.length === 0) {
            container.innerHTML = '<p>Nenhuma recomendação encontrada.</p>';
            return;
        }
        
        items.forEach((item, index) => {
            const card = this.createMediaCard(item, tipo, index);
            container.appendChild(card);
        });
    }
    
    createMediaCard(item, tipo, index) {
        // Container principal (agora é um link!)
        const card = document.createElement('a');
        card.href = item.link_url;
        card.target = '_blank';  // Abre em nova aba
        card.className = 'content-card media-card';
        card.rel = 'noopener noreferrer';  // Segurança
        
        // Wrapper da imagem
        const imageWrapper = document.createElement('div');
        imageWrapper.className = 'media-image-wrapper';
        
        // Imagem de capa
        const img = document.createElement('img');
        img.src = item.imagem_url;
        img.alt = item.titulo;
        img.className = 'media-image';
        img.loading = 'lazy';  // Lazy loading
        
        // Fallback se a imagem não carregar
        img.onerror = () => {
            img.src = this.getPlaceholderImage(tipo);
        };
        
        imageWrapper.appendChild(img);
        
        // Badge de relevância (overlay na imagem)
        const badge = document.createElement('div');
        badge.className = 'relevancia-badge';
        badge.textContent = `${item.relevancia}/10`;
        
        // Cor da badge baseada no score
        if (item.relevancia >= 9) {
            badge.style.background = '#10b981';
        } else if (item.relevancia >= 7) {
            badge.style.background = '#f59e0b';
        } else {
            badge.style.background = '#6366f1';
        }
        
        imageWrapper.appendChild(badge);
        
        // Info do conteúdo
        const infoDiv = document.createElement('div');
        infoDiv.className = 'media-info';
        
        // Título
        const title = document.createElement('div');
        title.className = 'media-title';
        title.textContent = item.titulo;
        
        // Subtítulo
        const subtitle = document.createElement('div');
        subtitle.className = 'media-subtitle';
        
        if (tipo === 'musica') {
            subtitle.textContent = item.artista;
        } else if (tipo === 'filme') {
            subtitle.textContent = `${item.diretor} (${item.ano})`;
        } else if (tipo === 'jogo') {
            subtitle.textContent = item.plataforma;
        }
        
        // Detalhes extras
        const details = document.createElement('div');
        details.className = 'media-details';
        
        if (tipo === 'musica') {
            details.innerHTML = `
                <span class="detail-item">🎵 ${item.genero}</span>
                <span class="detail-item">⏱️ ${item.duracao}</span>
            `;
        } else if (tipo === 'filme') {
            details.innerHTML = `
                <span class="detail-item">🎬 ${item.genero}</span>
                <span class="detail-item">⏱️ ${item.duracao}</span>
            `;
        } else if (tipo === 'jogo') {
            details.innerHTML = `
                <span class="detail-item">🎮 ${item.genero}</span>
                <span class="detail-item">${item.multiplayer ? '👥 Multi' : '👤 Single'}</span>
            `;
        }
        
        // Ícone de link externo
        const linkIcon = document.createElement('div');
        linkIcon.className = 'external-link-icon';
        linkIcon.innerHTML = '🔗';
        linkIcon.title = 'Clique para abrir';
        
        // Monta o card
        infoDiv.appendChild(title);
        infoDiv.appendChild(subtitle);
        infoDiv.appendChild(details);
        
        card.appendChild(imageWrapper);
        card.appendChild(infoDiv);
        card.appendChild(linkIcon);
        
        // Animação de entrada
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 50 + (index * 100));  // Animação em cascata
        
        return card;
    }
    
    getPlaceholderImage(tipo) {
        // Imagens placeholder caso não carregue
        const placeholders = {
            'musica': 'https://via.placeholder.com/300x300/667eea/ffffff?text=🎵+Música',
            'filme': 'https://via.placeholder.com/300x450/764ba2/ffffff?text=🎬+Filme',
            'jogo': 'https://via.placeholder.com/460x215/f093fb/ffffff?text=🎮+Jogo'
        };
        return placeholders[tipo] || 'https://via.placeholder.com/300x300/gray/ffffff?text=?';
    }
    
    showLoading() {
        this.moodSelector.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.loadingSection.style.display = 'block';
    }
    
    showResults() {
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
        
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    
    showMoodSelector() {
        this.resultsSection.style.display = 'none';
        this.loadingSection.style.display = 'none';
        this.moodSelector.style.display = 'block';
        
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Inicializa
document.addEventListener('DOMContentLoaded', () => {
    new MoodRecommenderWithMedia();
});