# 🎧 Mood-Based Recommender

Sistema inteligente de recomendação de conteúdo baseado no humor do usuário.

## 📋 Descrição

O Mood-Based Recommender é uma aplicação web que recomenda músicas, filmes e jogos personalizados com base no estado emocional atual do usuário. Utilizando um algoritmo de pontuação por humor, o sistema seleciona o conteúdo mais adequado para cada emoção.

## ✨ Funcionalidades

- **6 Estados de Humor**: Feliz, Triste, Relaxado, Energizado, Ansioso e Pensativo
- **Recomendações Múltiplas**: Músicas, Filmes e Jogos
- **Interface Intuitiva**: Design moderno e responsivo
- **Sistema de Relevância**: Pontuação de 0-10 para cada recomendação
- **API RESTful**: Endpoints para integração

## 🚀 Como Usar

### Instalação

```bash
# Clone o repositório (ou use os arquivos fornecidos)
cd mood-recommender

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
python mood_recommender.py
```

### Acesso

Abra seu navegador e acesse:
```
http://localhost:5000
```

## 🏗️ Estrutura do Projeto

```
mood-recommender/
│
├── mood_recommender.py       # Aplicação principal Flask
├── requirements.txt          # Dependências Python
│
├── templates/
│   └── index.html           # Interface web
│
└── static/
    ├── css/
    │   └── style.css        # Estilos CSS
    └── js/
        └── app.js           # JavaScript client-side
```

## 🎯 Como Funciona

### Algoritmo de Recomendação

Cada item de conteúdo possui scores de 0-10 para cada humor:

```python
Musica(
    titulo="Don't Stop Me Now",
    artista="Queen",
    mood_scores={
        "feliz": 10,      # Perfeito para humor feliz
        "energizado": 9,  # Ótimo para energia
        "relaxado": 2     # Não adequado para relaxamento
    }
)
```

O sistema:
1. Recebe o humor selecionado pelo usuário
2. Busca todos os itens no banco de dados
3. Ordena por score do humor selecionado
4. Retorna os top 3-5 itens de cada categoria

### Base de Dados

**Atual (MVP)**:
- 10 músicas
- 10 filmes
- 10 jogos

**Próximos Passos**:
- Expandir para 100+ itens por categoria
- Adicionar banco de dados SQL
- Implementar sistema de preferências do usuário

## 🔌 API Endpoints

### GET /api/moods
Retorna lista de humores disponíveis
```json
[
  {"id": "feliz", "nome": "😄 Feliz", "emoji": "😄"},
  {"id": "triste", "nome": "😔 Triste", "emoji": "😔"}
]
```

### POST /api/recomendar
Solicita recomendações para um humor específico

**Request:**
```json
{
  "mood": "feliz",
  "tipo": "tudo"  // ou "musicas", "filmes", "jogos"
}
```

**Response:**
```json
{
  "mood": "feliz",
  "musicas": [...],
  "filmes": [...],
  "jogos": [...]
}
```

## 🎨 Personalização

### Adicionar Novo Conteúdo

Edite o arquivo `mood_recommender.py`:

```python
def _carregar_musicas(self):
    return [
        Musica(
            id=11,
            titulo="Nova Música",
            mood_scores={"feliz": 8, "energizado": 7},
            artista="Artista",
            duracao="3:30",
            genero="Pop"
        ),
        # ... mais músicas
    ]
```

### Adicionar Novo Humor

1. Adicione ao enum `Mood`:
```python
class Mood(Enum):
    EMPOLGADO = "🤩 Empolgado"
```

2. Adicione scores nos itens de conteúdo:
```python
mood_scores={"feliz": 9, "empolgado": 10}
```

3. Adicione botão no HTML e CSS conforme necessário

## 📊 Roadmap

### Fase 1: MVP ✅
- [x] Interface básica
- [x] 6 humores
- [x] Algoritmo de recomendação
- [x] 30 itens de conteúdo

### Fase 2: Melhorias (Próximos Passos)
- [ ] Histórico de seleções do usuário
- [ ] Sistema de feedback (curtir/não curtir)
- [ ] Banco de dados SQL
- [ ] 100+ itens por categoria
- [ ] Integração Spotify API

### Fase 3: Machine Learning
- [ ] Coletar dados de preferências
- [ ] Treinar modelo de recomendação
- [ ] Personalização por usuário
- [ ] Recomendações híbridas (conteúdo + colaborativo)

## 🛠️ Tecnologias

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Gradientes modernos, animações CSS

## 📝 Licença

Este é um projeto de demonstração. Sinta-se livre para usar e modificar.

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Algumas ideias:

1. Adicionar mais conteúdo à base de dados
2. Implementar autenticação de usuários
3. Criar testes automatizados
4. Adicionar integração com APIs externas (Spotify, TMDB, IGDB)
5. Implementar busca por texto

## 📧 Contato

Para dúvidas ou sugestões sobre o projeto, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Python + Flask**
