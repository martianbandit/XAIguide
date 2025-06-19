Ce serveur MCP (Model Context Protocol) permet d'interagir avec l'API Reddit via Claude Desktop ou d'autres clients MCP.

## Fonctionnalités

Le serveur expose les outils suivants :

1. **get_subreddit_posts** - Récupère les posts d'un subreddit
2. **get_post_comments** - Récupère les commentaires d'un post spécifique
3. **search_reddit** - Effectue une recherche sur Reddit
4. **get_subreddit_info** - Obtient les informations d'un subreddit
5. **get_popular_subreddits** - Liste les subreddits populaires

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Un compte développeur Reddit
- uv (gestionnaire de paquets Python) : https://docs.astral.sh/uv/

### Configuration Reddit API

1. Allez sur https://www.reddit.com/prefs/apps
2. Cliquez sur "Create App" ou "Create Another App"
3. Remplissez les champs :
   - **name** : Un nom pour votre application
   - **App type** : Sélectionnez "script"
   - **description** : Description de votre app (optionnel)
   - **about url** : URL de votre app (optionnel)
   - **redirect uri** : http://localhost:8080 (requis même si pas utilisé)
4. Cliquez sur "Create app"
5. Notez votre **client ID** (sous le nom de l'app) et **client secret**

### Installation du serveur

```bash
# Créer le répertoire du projet
mkdir reddit-mcp-server
cd reddit-mcp-server

# Créer l'environnement virtuel avec uv
uv init
uv add fastmcp aiohttp pydantic

# Copier le code du serveur dans reddit_server.py
# Copier le fichier .env.example vers .env et configurer vos identifiants
cp .env.example .env
# Éditez .env avec vos vraies valeurs
```

### Configuration des variables d'environnement

Créez un fichier `.env` avec vos identifiants Reddit :

```bash
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_client_secret
REDDIT_USER_AGENT=MCP Reddit Server 1.0
```

## Utilisation avec Claude Desktop

### Configuration de Claude Desktop

1. Ouvrez le fichier de configuration Claude Desktop :
   - **macOS** : `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows** : `%APPDATA%\Claude\claude_desktop_config.json`

2. Ajoutez la configuration du serveur Reddit :

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uv",
      "args": [
        "--directory",
        "/CHEMIN/ABSOLU/VERS/reddit-mcp-server",
        "run",
        "reddit_server.py"
      ],
      "env": {
        "REDDIT_CLIENT_ID": "votre_client_id",
        "REDDIT_CLIENT_SECRET": "votre_client_secret",
        "REDDIT_USER_AGENT": "MCP Reddit Server 1.0"
      }
    }
  }
}
```

3. Remplacez `/CHEMIN/ABSOLU/VERS/reddit-mcp-server` par le chemin complet vers votre dossier du serveur.

4. Redémarrez Claude Desktop.

### Test du serveur

Une fois configuré, vous devriez voir l'icône marteau (🔨) dans Claude Desktop, indiquant que les outils MCP sont disponibles.

Vous pouvez tester avec des commandes comme :
- "Quels sont les posts populaires sur r/python ?"
- "Recherche des posts sur l'IA dans r/MachineLearning"
- "Montre-moi les informations du subreddit r/programming"
- "Quels sont les subreddits populaires actuellement ?"

## Exemples d'utilisation

### Récupérer les posts populaires d'un subreddit
```
Montre-moi les 10 posts les plus populaires de r/technology aujourd'hui
```

### Rechercher du contenu spécifique
```
Recherche des posts parlant de "ChatGPT" dans r/artificial
```

### Obtenir les commentaires d'un post
```
Récupère les commentaires du post avec l'ID abc123 de r/programming
```

### Informations sur un subreddit
```
Donne-moi les informations sur le subreddit r/MachineLearning
```

## Dépannage

### Le serveur ne se connecte pas
- Vérifiez que les variables d'environnement sont correctement configurées
- Assurez-vous que les identifiants Reddit sont valides
- Vérifiez les logs dans Claude Desktop (Menu Aide > Afficher les logs)

### Erreurs d'authentification
- Vérifiez que votre client ID et secret sont corrects
- Assurez-vous que votre application Reddit est de type "script"
- Le User-Agent doit être unique et descriptif

### Limitation de taux
Reddit limite le nombre de requêtes par minute. Si vous atteignez la limite, attendez quelques minutes avant de réessayer.

## Sécurité

- Ne partagez jamais vos identifiants Reddit
- Utilisez un User-Agent descriptif et unique
- Respectez les conditions d'utilisation de Reddit
- Le serveur utilise uniquement l'authentification en lecture seule

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.