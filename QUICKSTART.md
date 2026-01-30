# 🚀 GUIA RÁPIDO - Mood-Based Recommender

## Início Rápido (3 passos)

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar o Servidor
```bash
python mood_recommender.py
```

### 3️⃣ Acessar no Navegador
```
http://localhost:5000
```

---

## 🧪 Testar sem Interface Web

Se quiser testar o sistema sem abrir o navegador:

```bash
python test_recommender.py
```

Isso vai:
- ✅ Mostrar recomendações para todos os 6 humores
- ✅ Testar as 3 categorias (músicas, filmes, jogos)
- ✅ Exportar dados para JSON

---

## 📁 Arquivos do Projeto

```
mood-recommender/
├── mood_recommender.py      ← Aplicação principal (Flask + Lógica)
├── test_recommender.py      ← Script de teste
├── requirements.txt         ← Dependências
├── README.md               ← Documentação completa
├── QUICKSTART.md           ← Este arquivo
│
├── templates/
│   └── index.html          ← Interface web
│
└── static/
    ├── css/
    │   └── style.css       ← Estilos
    └── js/
        └── app.js          ← JavaScript
```

---

## 🎯 Exemplos de Uso

### Uso Web (Recomendado)
1. Execute: `python mood_recommender.py`
2. Abra: `http://localhost:5000`
3. Clique em um emoji de humor
4. Veja suas recomendações personalizadas!

### Uso via API (Python)
```python
from mood_recommender import MoodRecommender

# Cria o recommender
rec = MoodRecommender()

# Busca recomendações para humor "feliz"
resultado = rec.recomendar_tudo("feliz")

# Acessa as recomendações
print(resultado['musicas'])  # Lista de músicas
print(resultado['filmes'])   # Lista de filmes
print(resultado['jogos'])    # Lista de jogos
```

### Uso via API (HTTP)
```bash
# Recomendações para humor "feliz"
curl -X POST http://localhost:5000/api/recomendar \
  -H "Content-Type: application/json" \
  -d '{"mood": "feliz", "tipo": "tudo"}'
```

---

## 🎨 Personalizar Conteúdo

### Adicionar Nova Música

Edite `mood_recommender.py` na função `_carregar_musicas()`:

```python
Musica(
    id=11,  # Próximo ID disponível
    titulo="Sua Música",
    mood_scores={
        "feliz": 9,
        "energizado": 8,
        "relaxado": 3
    },
    artista="Nome do Artista",
    duracao="3:45",
    genero="Rock"
)
```

### Adicionar Novo Filme

Edite `mood_recommender.py` na função `_carregar_filmes()`:

```python
Filme(
    id=11,
    titulo="Seu Filme",
    mood_scores={
        "pensativo": 10,
        "triste": 7
    },
    diretor="Nome do Diretor",
    ano=2024,
    genero="Drama",
    duracao="120 min"
)
```

---

## 🐛 Problemas Comuns

### Porta 5000 já está em uso
```bash
# Use outra porta
python mood_recommender.py
# Edite no código: app.run(port=5001)
```

### Erro ao importar Flask
```bash
pip install Flask --break-system-packages
# ou
pip install -r requirements.txt --break-system-packages
```

---

## 📊 Estatísticas do Sistema

- **6 Humores**: Feliz, Triste, Relaxado, Energizado, Ansioso, Pensativo
- **30 Itens**: 10 músicas + 10 filmes + 10 jogos
- **Top 3**: Mostra as 3 melhores recomendações de cada categoria
- **Score 0-10**: Sistema de pontuação de relevância

---

## 🔥 Próximos Passos

Depois de testar o sistema básico, você pode:

1. **Expandir a Base de Dados**: Adicione mais músicas, filmes e jogos
2. **Adicionar Banco de Dados**: Migre para SQLite ou PostgreSQL
3. **Implementar Usuários**: Sistema de login e preferências
4. **Integrar APIs**: Spotify, TMDB, IGDB
5. **Machine Learning**: Treinar modelo de recomendação personalizado

---

## 💡 Dicas

- **Scores**: Use 8-10 para alta compatibilidade, 5-7 para média, 0-4 para baixa
- **Múltiplos Moods**: Um item pode ter bom score em vários humores
- **Balanceamento**: Tente ter pelo menos 3 itens com score 8+ para cada humor

---

## 🆘 Ajuda

- **README.md**: Documentação completa
- **test_recommender.py**: Exemplos de uso
- **Código comentado**: Leia os comentários no código

---

**Bom uso! 🎉**
