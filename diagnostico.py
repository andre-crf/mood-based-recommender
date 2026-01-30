#!/usr/bin/env python3
"""
Script de Diagnóstico - Mood-Based Recommender
Verifica se tudo está funcionando corretamente
"""

import sys

print("="*60)
print("🔍 DIAGNÓSTICO DO SISTEMA")
print("="*60)
print()

# 1. Verifica versão do Python
print("1️⃣ Verificando versão do Python...")
print(f"   Versão: {sys.version}")
if sys.version_info < (3, 7):
    print("   ⚠️  AVISO: Python 3.7+ é recomendado")
else:
    print("   ✅ Versão OK")
print()

# 2. Verifica imports
print("2️⃣ Verificando imports necessários...")
try:
    import flask
    print(f"   ✅ Flask {flask.__version__} instalado")
except ImportError:
    print("   ❌ Flask NÃO instalado!")
    print("      Execute: pip install Flask")
    sys.exit(1)

try:
    from dataclasses import dataclass
    print("   ✅ dataclasses disponível")
except ImportError:
    print("   ❌ dataclasses não disponível (Python < 3.7)")
    sys.exit(1)

print()

# 3. Verifica estrutura de arquivos
print("3️⃣ Verificando estrutura de arquivos...")
import os

arquivos_necessarios = [
    'mood_recommender.py',
    'templates/index.html',
    'static/css/style.css',
    'static/js/app.js'
]

tudo_ok = True
for arquivo in arquivos_necessarios:
    if os.path.exists(arquivo):
        print(f"   ✅ {arquivo}")
    else:
        print(f"   ❌ {arquivo} NÃO ENCONTRADO")
        tudo_ok = False

if not tudo_ok:
    print("\n   ⚠️  Alguns arquivos estão faltando!")
    print("      Certifique-se de estar no diretório correto do projeto")
print()

# 4. Testa importação do módulo
print("4️⃣ Testando importação do módulo...")
try:
    from mood_recommender import MoodRecommender
    print("   ✅ Módulo importado com sucesso")
    
    # Testa instanciação
    rec = MoodRecommender()
    print(f"   ✅ Recommender instanciado")
    print(f"   📊 {len(rec.musicas)} músicas carregadas")
    print(f"   📊 {len(rec.filmes)} filmes carregados")
    print(f"   📊 {len(rec.jogos)} jogos carregados")
except Exception as e:
    print(f"   ❌ Erro ao importar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 5. Testa recomendação
print("5️⃣ Testando sistema de recomendação...")
try:
    resultado = rec.recomendar_tudo("feliz")
    print(f"   ✅ Recomendações para 'feliz' geradas")
    print(f"   📊 {len(resultado['musicas'])} músicas recomendadas")
    print(f"   📊 {len(resultado['filmes'])} filmes recomendados")
    print(f"   📊 {len(resultado['jogos'])} jogos recomendados")
    
    # Mostra primeira música
    if resultado['musicas']:
        primeira = resultado['musicas'][0]
        print(f"\n   Exemplo: {primeira['titulo']} - {primeira['artista']}")
        print(f"   Relevância: {primeira['relevancia']}/10")
        
except Exception as e:
    print(f"   ❌ Erro ao gerar recomendações: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 6. Verifica porta
print("6️⃣ Verificando disponibilidade da porta 5000...")
import socket

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

if check_port(5000):
    print("   ✅ Porta 5000 está disponível")
else:
    print("   ⚠️  Porta 5000 já está em uso")
    print("      Você pode precisar matar o processo ou usar outra porta")

print()
print("="*60)
print("✅ DIAGNÓSTICO COMPLETO!")
print("="*60)
print()
print("Para iniciar o servidor, execute:")
print("  python mood_recommender.py")
print()
print("Depois acesse no navegador:")
print("  http://localhost:5000")
print()
print("Para testar o health check:")
print("  http://localhost:5000/health")
print()