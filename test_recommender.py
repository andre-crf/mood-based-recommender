#!/usr/bin/env python3
"""
Script de teste para demonstrar o uso da API do Mood Recommender
"""

from mood_recommender import MoodRecommender
import json

def test_recommender():
    """Testa o sistema de recomendação"""
    
    print("=" * 60)
    print("🎧 MOOD-BASED RECOMMENDER - TESTE DO SISTEMA")
    print("=" * 60)
    print()
    
    # Inicializa o recommender
    recommender = MoodRecommender()
    
    # Lista de moods para testar
    moods = ["feliz", "triste", "relaxado", "energizado", "ansioso", "pensativo"]
    
    # Testa cada mood
    for mood in moods:
        print(f"\n{'='*60}")
        print(f"🎭 HUMOR: {mood.upper()}")
        print('='*60)
        
        # Busca recomendações
        resultado = recommender.recomendar_tudo(mood)
        
        # Exibe músicas
        print("\n🎵 MÚSICAS:")
        print("-" * 60)
        for musica in resultado['musicas']:
            print(f"  • {musica['titulo']} - {musica['artista']}")
            print(f"    Relevância: {musica['relevancia']}/10 | Gênero: {musica['genero']}")
        
        # Exibe filmes
        print("\n🎬 FILMES:")
        print("-" * 60)
        for filme in resultado['filmes']:
            print(f"  • {filme['titulo']} ({filme['ano']})")
            print(f"    Diretor: {filme['diretor']} | Relevância: {filme['relevancia']}/10")
        
        # Exibe jogos
        print("\n🎮 JOGOS:")
        print("-" * 60)
        for jogo in resultado['jogos']:
            mp = "Multiplayer" if jogo['multiplayer'] else "Single Player"
            print(f"  • {jogo['titulo']}")
            print(f"    {jogo['plataforma']} | {mp} | Relevância: {jogo['relevancia']}/10")


def test_individual_categories():
    """Testa categorias individuais"""
    
    print("\n\n" + "=" * 60)
    print("📊 TESTE DE CATEGORIAS INDIVIDUAIS")
    print("=" * 60)
    
    recommender = MoodRecommender()
    
    # Teste: Músicas para humor feliz
    print("\n🎵 Top 5 Músicas para Humor FELIZ:")
    print("-" * 60)
    musicas = recommender.recomendar("feliz", "musicas", 5)
    for i, musica in enumerate(musicas, 1):
        print(f"{i}. {musica['titulo']} - {musica['artista']} [{musica['relevancia']}/10]")
    
    # Teste: Filmes para humor pensativo
    print("\n🎬 Top 5 Filmes para Humor PENSATIVO:")
    print("-" * 60)
    filmes = recommender.recomendar("pensativo", "filmes", 5)
    for i, filme in enumerate(filmes, 1):
        print(f"{i}. {filme['titulo']} ({filme['ano']}) [{filme['relevancia']}/10]")
    
    # Teste: Jogos para humor energizado
    print("\n🎮 Top 5 Jogos para Humor ENERGIZADO:")
    print("-" * 60)
    jogos = recommender.recomendar("energizado", "jogos", 5)
    for i, jogo in enumerate(jogos, 1):
        print(f"{i}. {jogo['titulo']} - {jogo['genero']} [{jogo['relevancia']}/10]")


def export_to_json():
    """Exporta todas as recomendações para JSON"""
    
    print("\n\n" + "=" * 60)
    print("💾 EXPORTANDO DADOS PARA JSON")
    print("=" * 60)
    
    recommender = MoodRecommender()
    moods = ["feliz", "triste", "relaxado", "energizado", "ansioso", "pensativo"]
    
    export_data = {}
    for mood in moods:
        export_data[mood] = recommender.recomendar_tudo(mood)
    
    # Salva em arquivo
    filename = "recomendacoes_export.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Dados exportados para: {filename}")
    print(f"📦 Total de {len(moods)} humores exportados")


if __name__ == "__main__":
    # Executa todos os testes
    test_recommender()
    test_individual_categories()
    export_to_json()
    
    print("\n\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    print("\nPara iniciar o servidor web, execute:")
    print("  python mood_recommender.py")
    print("\nDepois acesse: http://localhost:5000")
    print()
