"""
Mood-Based Recommender - VERSÃO COM IMAGENS E LINKS

Melhorias:
- Imagens de capa para músicas, filmes e jogos
- Links clicáveis para Spotify, YouTube, IMDb, Steam, etc.
- URLs de busca automática
- Layout visual aprimorado
"""

from flask import Flask, render_template, request, jsonify, session
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import traceback
import random
from datetime import datetime
import urllib.parse

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui-mude-em-producao'

class Mood(Enum):
    FELIZ = "😄 Feliz"
    TRISTE = "😔 Triste"
    RELAXADO = "😴 Relaxado"
    ENERGIZADO = "😡 Energizado"
    ANSIOSO = "😰 Ansioso"
    PENSATIVO = "🤔 Pensativo"

@dataclass
class ConteudoBase:
    id: int
    titulo: str
    mood_scores: Dict[str, int]
    imagem_url: str  # Nova propriedade
    link_url: str    # Nova propriedade
    
@dataclass
class Musica(ConteudoBase):
    artista: str
    duracao: str
    genero: str
    spotify_id: Optional[str] = None  # ID do Spotify
    youtube_url: Optional[str] = None  # URL do YouTube
    
@dataclass
class Filme(ConteudoBase):
    diretor: str
    ano: int
    genero: str
    duracao: str
    imdb_id: Optional[str] = None  # ID do IMDb
    
@dataclass
class Jogo(ConteudoBase):
    plataforma: str
    genero: str
    multiplayer: bool
    steam_id: Optional[str] = None  # ID da Steam


class MoodRecommenderWithMedia:
    """Engine de recomendação com imagens e links"""
    
    def __init__(self):
        self.musicas = self._carregar_musicas()
        self.filmes = self._carregar_filmes()
        self.jogos = self._carregar_jogos()
    
    def _gerar_url_busca_youtube(self, artista: str, titulo: str) -> str:
        """Gera URL de busca no YouTube"""
        query = f"{artista} {titulo}"
        return f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    def _gerar_url_spotify(self, artista: str, titulo: str) -> str:
        """Gera URL de busca no Spotify"""
        query = f"{artista} {titulo}"
        return f"https://open.spotify.com/search/{urllib.parse.quote(query)}"
    
    def _gerar_url_imdb(self, titulo: str, ano: int = None) -> str:
        """Gera URL de busca no IMDb"""
        query = f"{titulo} {ano}" if ano else titulo
        return f"https://www.imdb.com/find?q={urllib.parse.quote(query)}"
    
    def _gerar_url_steam(self, titulo: str) -> str:
        """Gera URL de busca na Steam"""
        return f"https://store.steampowered.com/search/?term={urllib.parse.quote(titulo)}"
    
    def _carregar_musicas(self) -> List[Musica]:
        """Músicas com imagens e links"""
        return [
            # Músicas FELIZES
            Musica(
                1, "Don't Stop Me Now", 
                {"feliz": 10, "energizado": 9, "relaxado": 2},
                "https://i.scdn.co/image/ab67616d0000b2731dacfbc31cc873d132958af9",  # Imagem do álbum Queen
                "https://open.spotify.com/track/7hQJA50XrCWABAu5v6QZ4i",
                "Queen", "3:29", "Rock",
                spotify_id="7hQJA50XrCWABAu5v6QZ4i"
            ),
            Musica(
                2, "Happy", 
                {"feliz": 10, "energizado": 8, "relaxado": 4},
                "https://i.scdn.co/image/ab67616d0000b2732c430aa917d49c0e48201f96",
                "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH",
                "Pharrell Williams", "3:53", "Pop",
                spotify_id="60nZcImufyMA1MKQY3dcCH"
            ),
            Musica(
                3, "Uptown Funk",
                {"feliz": 9, "energizado": 10, "relaxado": 2},
                "https://i.scdn.co/image/ab67616d0000b273e787cffec20aa2a396a61647",
                "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS",
                "Bruno Mars", "4:30", "Funk",
                spotify_id="32OlwWuMpZ6b0aN2RZOeMS"
            ),
            Musica(
                4, "Walking on Sunshine",
                {"feliz": 10, "energizado": 8, "relaxado": 3},
                "https://i.scdn.co/image/ab67616d0000b27328913659e89e2af74e4a86be",
                "https://open.spotify.com/track/05wIrZSwuaVWhcv5FfqeH0",
                "Katrina and the Waves", "3:59", "Pop"
            ),
            Musica(
                5, "September",
                {"feliz": 10, "energizado": 8, "relaxado": 4},
                "https://i.scdn.co/image/ab67616d0000b273b265cb78606ecf7c58a7b122",
                "https://open.spotify.com/track/2grjqo0Frpf2okIBiifQKs",
                "Earth, Wind & Fire", "3:35", "Funk"
            ),
            
            # Músicas TRISTES
            Musica(
                6, "Someone Like You",
                {"triste": 10, "pensativo": 8, "relaxado": 6},
                "https://i.scdn.co/image/ab67616d0000b273372d1e7c417f8b4a86564129",
                "https://open.spotify.com/track/1zwMYTA5nlNjZxYrvBB2pV",
                "Adele", "4:45", "Pop"
            ),
            Musica(
                7, "Fix You",
                {"triste": 8, "pensativo": 9, "feliz": 6},
                "https://i.scdn.co/image/ab67616d0000b2732493500e08fd8c0a8c0d7acc",
                "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q",
                "Coldplay", "4:54", "Alternative"
            ),
            
            # Músicas RELAXADAS
            Musica(
                8, "Weightless",
                {"relaxado": 10, "ansioso": 8, "pensativo": 7},
                "https://i.scdn.co/image/ab67616d0000b273c8b444df094279e70d0ed856",
                "https://open.spotify.com/track/6XH9zFFH6WkGD5d0uh7yRh",
                "Marconi Union", "8:00", "Ambient"
            ),
            Musica(
                9, "Clair de Lune",
                {"relaxado": 10, "pensativo": 9, "triste": 5},
                "https://i.scdn.co/image/ab67616d0000b2739f98ea31b68cd83bbf5ad70a",
                "https://open.spotify.com/track/1mCsF9Tw5freNjo4jWdHMu",
                "Debussy", "5:00", "Clássica"
            ),
            
            # Músicas ENERGIZADAS
            Musica(
                10, "Eye of the Tiger",
                {"energizado": 10, "feliz": 7, "ansioso": 3},
                "https://i.scdn.co/image/ab67616d0000b273dd9c9e498e4c00407cc12a61",
                "https://open.spotify.com/track/2KH16WveTQWT6KOG9Rg6e2",
                "Survivor", "4:05", "Rock"
            ),
        ]
    
    def _carregar_filmes(self) -> List[Filme]:
        """Filmes com posters e links do IMDb"""
        return [
            # Filmes FELIZES
            Filme(
                1, "The Grand Budapest Hotel",
                {"feliz": 9, "pensativo": 7, "relaxado": 6},
                "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt2278388/",
                "Wes Anderson", 2014, "Comédia", "99 min",
                imdb_id="tt2278388"
            ),
            Filme(
                2, "Amélie",
                {"feliz": 10, "pensativo": 7, "relaxado": 8},
                "https://m.media-amazon.com/images/M/MV5BNDg4NjM1YjMtYmNhZC00MjM0LWFiZmYtNGY1YjA3MzZmODc5XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt0211915/",
                "Jean-Pierre Jeunet", 2001, "Romance/Comédia", "122 min",
                imdb_id="tt0211915"
            ),
            Filme(
                3, "Guardians of the Galaxy",
                {"feliz": 9, "energizado": 8, "relaxado": 5},
                "https://m.media-amazon.com/images/M/MV5BNzM3NDFhYTQtYjViOC00NDZhLWI0Y2ItZGUyZGMxODdjMmU1XkEyXkFqcGc@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt2015381/",
                "James Gunn", 2014, "Ação/Comédia", "121 min",
                imdb_id="tt2015381"
            ),
            
            # Filmes TRISTES
            Filme(
                4, "The Pursuit of Happyness",
                {"feliz": 8, "pensativo": 9, "triste": 7},
                "https://m.media-amazon.com/images/M/MV5BMTQ5NjQ0NDI3NF5BMl5BanBnXkFtZTcwNDI0MjEzMw@@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt0454921/",
                "Gabriele Muccino", 2006, "Drama", "117 min",
                imdb_id="tt0454921"
            ),
            Filme(
                5, "Eternal Sunshine of the Spotless Mind",
                {"triste": 9, "pensativo": 10, "relaxado": 4},
                "https://m.media-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt0338013/",
                "Michel Gondry", 2004, "Romance/Drama", "108 min",
                imdb_id="tt0338013"
            ),
            
            # Filmes PENSATIVOS
            Filme(
                6, "Blade Runner 2049",
                {"pensativo": 10, "triste": 7, "ansioso": 6},
                "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt1856101/",
                "Denis Villeneuve", 2017, "Sci-Fi", "164 min",
                imdb_id="tt1856101"
            ),
            Filme(
                7, "Arrival",
                {"pensativo": 10, "ansioso": 7, "triste": 6},
                "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_SX300.jpg",
                "https://www.imdb.com/title/tt2543164/",
                "Denis Villeneuve", 2016, "Sci-Fi", "116 min",
                imdb_id="tt2543164"
            ),
            
            # Filmes ENERGIZADOS
            Filme(
                8, "Mad Max: Fury Road",
                {"energizado": 10, "ansioso": 8, "feliz": 6},
                "https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt1392190/",
                "George Miller", 2015, "Ação", "120 min",
                imdb_id="tt1392190"
            ),
            Filme(
                9, "John Wick",
                {"energizado": 10, "ansioso": 5, "feliz": 4},
                "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt2911666/",
                "Chad Stahelski", 2014, "Ação", "101 min",
                imdb_id="tt2911666"
            ),
            
            # Filmes RELAXANTES
            Filme(
                10, "My Neighbor Totoro",
                {"relaxado": 10, "feliz": 9, "pensativo": 5},
                "https://m.media-amazon.com/images/M/MV5BYzJjMTYyMjQtZDI0My00ZjE2LTkyNGYtOTllNGQxNDMyZjE0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "https://www.imdb.com/title/tt0096283/",
                "Hayao Miyazaki", 1988, "Animação", "86 min",
                imdb_id="tt0096283"
            ),
        ]
    
    def _carregar_jogos(self) -> List[Jogo]:
        """Jogos com imagens e links"""
        return [
            # Jogos RELAXANTES
            Jogo(
                1, "Stardew Valley",
                {"relaxado": 10, "feliz": 8, "pensativo": 6},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg",
                "https://store.steampowered.com/app/413150/Stardew_Valley/",
                "PC/Console", "Simulação", False,
                steam_id="413150"
            ),
            Jogo(
                2, "Animal Crossing: New Horizons",
                {"relaxado": 10, "feliz": 9, "pensativo": 5},
                "https://assets.nintendo.com/image/upload/f_auto/q_auto/dpr_2.0/c_scale,w_500/ncom/en_US/games/switch/a/animal-crossing-new-horizons-switch/hero",
                "https://www.nintendo.com/games/detail/animal-crossing-new-horizons-switch/",
                "Nintendo Switch", "Simulação", False
            ),
            Jogo(
                3, "Journey",
                {"pensativo": 10, "relaxado": 9, "triste": 6},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/638230/header.jpg",
                "https://store.steampowered.com/app/638230/Journey/",
                "PlayStation/PC", "Aventura", True,
                steam_id="638230"
            ),
            
            # Jogos ENERGIZADOS
            Jogo(
                4, "DOOM Eternal",
                {"energizado": 10, "ansioso": 3, "feliz": 6},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/782330/header.jpg",
                "https://store.steampowered.com/app/782330/DOOM_Eternal/",
                "PC/Console", "FPS", False,
                steam_id="782330"
            ),
            Jogo(
                5, "Hades",
                {"energizado": 10, "feliz": 8, "ansioso": 5},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg",
                "https://store.steampowered.com/app/1145360/Hades/",
                "PC/Console", "Roguelike", False,
                steam_id="1145360"
            ),
            
            # Jogos FELIZES
            Jogo(
                6, "Mario Kart 8 Deluxe",
                {"feliz": 10, "energizado": 7, "relaxado": 4},
                "https://assets.nintendo.com/image/upload/f_auto/q_auto/dpr_2.0/c_scale,w_500/ncom/en_US/games/switch/m/mario-kart-8-deluxe-switch/hero",
                "https://www.nintendo.com/games/detail/mario-kart-8-deluxe-switch/",
                "Nintendo Switch", "Racing", True
            ),
            Jogo(
                7, "Fall Guys",
                {"feliz": 9, "energizado": 7, "relaxado": 5},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/1097150/header.jpg",
                "https://store.steampowered.com/app/1097150/Fall_Guys/",
                "PC/Console", "Party", True,
                steam_id="1097150"
            ),
            
            # Jogos PENSATIVOS
            Jogo(
                8, "Outer Wilds",
                {"pensativo": 10, "ansioso": 7, "feliz": 7},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/753640/header.jpg",
                "https://store.steampowered.com/app/753640/Outer_Wilds/",
                "PC/Console", "Aventura", False,
                steam_id="753640"
            ),
            Jogo(
                9, "What Remains of Edith Finch",
                {"pensativo": 10, "triste": 9, "relaxado": 5},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/501300/header.jpg",
                "https://store.steampowered.com/app/501300/What_Remains_of_Edith_Finch/",
                "PC/Console", "Narrativa", False,
                steam_id="501300"
            ),
            
            # Jogos EMOCIONAIS
            Jogo(
                10, "Celeste",
                {"ansioso": 7, "energizado": 8, "pensativo": 7},
                "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/header.jpg",
                "https://store.steampowered.com/app/504230/Celeste/",
                "PC/Console", "Plataforma", False,
                steam_id="504230"
            ),
        ]
    
    def recomendar_com_variedade(self, mood: str, tipo: str, limite: int = 3,
                                  historico_ids: List[int] = None) -> List[Dict]:
        """Recomenda com variedade (mesmo código anterior)"""
        mood = mood.lower()
        historico_ids = historico_ids or []
        
        if tipo == "musicas":
            conteudo = self.musicas
        elif tipo == "filmes":
            conteudo = self.filmes
        elif tipo == "jogos":
            conteudo = self.jogos
        else:
            return []
        
        candidatos = []
        for item in conteudo:
            score = item.mood_scores.get(mood, 0)
            if score >= 6 and item.id not in historico_ids:
                item_dict = asdict(item)
                item_dict['relevancia'] = score
                candidatos.append(item_dict)
        
        if not candidatos:
            for item in conteudo:
                score = item.mood_scores.get(mood, 0)
                if score >= 5:
                    item_dict = asdict(item)
                    item_dict['relevancia'] = score
                    candidatos.append(item_dict)
        
        tier_alto = [c for c in candidatos if c['relevancia'] >= 9]
        tier_medio = [c for c in candidatos if 7 <= c['relevancia'] < 9]
        tier_baixo = [c for c in candidatos if c['relevancia'] < 7]
        
        selecionados = []
        
        if tier_alto:
            random.shuffle(tier_alto)
            selecionados.extend(tier_alto[:min(2, limite)])
        
        if len(selecionados) < limite and tier_medio:
            random.shuffle(tier_medio)
            selecionados.extend(tier_medio[:limite - len(selecionados)])
        
        if len(selecionados) < limite and tier_baixo:
            random.shuffle(tier_baixo)
            selecionados.extend(tier_baixo[:limite - len(selecionados)])
        
        random.shuffle(selecionados)
        
        return selecionados[:limite]
    
    def recomendar_tudo_com_variedade(self, mood: str, session_data: Dict = None) -> Dict:
        """Recomenda tudo com histórico"""
        session_data = session_data or {}
        
        historico_musicas = session_data.get('historico_musicas', [])
        historico_filmes = session_data.get('historico_filmes', [])
        historico_jogos = session_data.get('historico_jogos', [])
        
        musicas = self.recomendar_com_variedade(mood, 'musicas', 3, historico_musicas)
        filmes = self.recomendar_com_variedade(mood, 'filmes', 3, historico_filmes)
        jogos = self.recomendar_com_variedade(mood, 'jogos', 3, historico_jogos)
        
        historico_musicas.extend([m['id'] for m in musicas])
        historico_filmes.extend([f['id'] for f in filmes])
        historico_jogos.extend([j['id'] for j in jogos])
        
        session_data['historico_musicas'] = historico_musicas[-15:]
        session_data['historico_filmes'] = historico_filmes[-15:]
        session_data['historico_jogos'] = historico_jogos[-15:]
        
        return {
            'mood': mood,
            'musicas': musicas,
            'filmes': filmes,
            'jogos': jogos,
            'session_data': session_data
        }


# Inicializa
recommender = MoodRecommenderWithMedia()

# Rotas (mesmas do anterior)
@app.route('/')
def index():
    return render_template('index.html', moods=Mood)

@app.route('/api/recomendar', methods=['POST'])
def api_recomendar():
    try:
        if 'session_data' not in session:
            session['session_data'] = {}
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Nenhum dado enviado'}), 400
        
        mood = data.get('mood', '').lower()
        tipo = data.get('tipo', 'tudo')
        
        if not mood:
            return jsonify({'erro': 'Mood não especificado'}), 400
        
        moods_validos = ['feliz', 'triste', 'relaxado', 'energizado', 'ansioso', 'pensativo']
        if mood not in moods_validos:
            return jsonify({'erro': 'Mood inválido'}), 400
        
        if tipo == 'tudo':
            resultado = recommender.recomendar_tudo_com_variedade(mood, session['session_data'])
            session['session_data'] = resultado.pop('session_data')
        else:
            historico = session['session_data'].get(f'historico_{tipo}', [])
            resultado = recommender.recomendar_com_variedade(mood, tipo, 3, historico)
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro: {e}")
        print(traceback.format_exc())
        return jsonify({'erro': 'Erro interno', 'mensagem': str(e)}), 500

@app.route('/api/moods')
def api_moods():
    try:
        moods = [{'id': m.name.lower(), 'nome': m.value, 'emoji': m.value.split()[0]} for m in Mood]
        return jsonify(moods)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'musicas': len(recommender.musicas),
        'filmes': len(recommender.filmes),
        'jogos': len(recommender.jogos),
        'versao': 'com_imagens_e_links'
    })

@app.route('/api/limpar-historico', methods=['POST'])
def limpar_historico():
    session['session_data'] = {}
    return jsonify({'sucesso': True, 'mensagem': 'Histórico limpo'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎧 MOOD RECOMMENDER - COM IMAGENS E LINKS")
    print("="*60)
    print(f"✅ Músicas: {len(recommender.musicas)}")
    print(f"✅ Filmes: {len(recommender.filmes)}")
    print(f"✅ Jogos: {len(recommender.jogos)}")
    print("\n🎯 RECURSOS:")
    print("  - Imagens de capa/poster")
    print("  - Links para Spotify, YouTube, IMDb, Steam")
    print("  - Sistema de variedade")
    print("  - Histórico anti-repetição")
    print("\n🌐 http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)