#!/usr/bin/env python3
#Serveur MCP pour l’API Reddit
#Ce serveur expose les fonctionnalités #principales de Reddit via le protocole MCP.


import os
import json
import logging
from typing import Optional, List, Dict, Any
import asyncio
import aiohttp
from datetime import datetime, timedelta
import base64

from fastmcp import FastMCP
from pydantic import BaseModel

# Configuration de logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(**name**)

# Instance FastMCP

mcp = FastMCP(“Reddit MCP Server”)

class RedditConfig:
“”“Configuration pour l’API Reddit”””
def **init**(self):
self.client_id = os.getenv(“REDDIT_CLIENT_ID”)
self.client_secret = os.getenv(“REDDIT_CLIENT_SECRET”)
self.user_agent = os.getenv(“REDDIT_USER_AGENT”, “MCP Reddit Server 1.0”)
self.base_url = “https://www.reddit.com”
self.api_url = “https://oauth.reddit.com”
self.auth_url = “https://www.reddit.com/api/v1/access_token”
self.access_token = None
self.token_expires = None

config = RedditConfig()

class RedditPost(BaseModel):
“”“Modèle pour un post Reddit”””
id: str
title: str
author: str
subreddit: str
score: int
num_comments: int
created_utc: float
url: str
selftext: Optional[str] = None
is_video: bool = False
over_18: bool = False

class RedditComment(BaseModel):
“”“Modèle pour un commentaire Reddit”””
id: str
author: str
body: str
score: int
created_utc: float
parent_id: str
is_submitter: bool = False

async def get_access_token() -> Optional[str]:
“”“Obtient un token d’accès pour l’API Reddit”””
if not config.client_id or not config.client_secret:
logger.error(“Client ID et Client Secret Reddit sont requis”)
return None

```
# Vérifier si le token est encore valide
if config.access_token and config.token_expires and datetime.now() < config.token_expires:
    return config.access_token

# Préparer les données d'authentification
auth_string = f"{config.client_id}:{config.client_secret}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "User-Agent": config.user_agent,
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials"
}

try:
    async with aiohttp.ClientSession() as session:
        async with session.post(config.auth_url, headers=headers, data=data) as response:
            if response.status == 200:
                token_data = await response.json()
                config.access_token = token_data["access_token"]
                expires_in = token_data.get("expires_in", 3600)
                config.token_expires = datetime.now() + timedelta(seconds=expires_in - 60)
                logger.info("Token d'accès Reddit obtenu avec succès")
                return config.access_token
            else:
                logger.error(f"Erreur lors de l'obtention du token: {response.status}")
                return None
except Exception as e:
    logger.error(f"Erreur lors de l'authentification Reddit: {e}")
    return None
```

async def make_reddit_request(endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
“”“Effectue une requête à l’API Reddit”””
token = await get_access_token()
if not token:
return None

```
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": config.user_agent
}

url = f"{config.api_url}{endpoint}"

try:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f"Erreur API Reddit: {response.status}")
                return None
except Exception as e:
    logger.error(f"Erreur lors de la requête Reddit: {e}")
    return None
```

def parse_reddit_post(post_data: Dict) -> RedditPost:
“”“Parse les données d’un post Reddit”””
data = post_data[“data”]
return RedditPost(
id=data[“id”],
title=data[“title”],
author=data[“author”],
subreddit=data[“subreddit”],
score=data[“score”],
num_comments=data[“num_comments”],
created_utc=data[“created_utc”],
url=data[“url”],
selftext=data.get(“selftext”, “”),
is_video=data.get(“is_video”, False),
over_18=data.get(“over_18”, False)
)

def parse_reddit_comment(comment_data: Dict) -> Optional[RedditComment]:
“”“Parse les données d’un commentaire Reddit”””
if comment_data[“kind”] != “t1”:
return None

```
data = comment_data["data"]
if data.get("body") == "[deleted]" or data.get("body") == "[removed]":
    return None

return RedditComment(
    id=data["id"],
    author=data.get("author", "[deleted]"),
    body=data["body"],
    score=data["score"],
    created_utc=data["created_utc"],
    parent_id=data["parent_id"],
    is_submitter=data.get("is_submitter", False)
)
```

@mcp.tool()
async def get_subreddit_posts(
subreddit: str,
sort: str = “hot”,
limit: int = 25,
time_filter: str = “all”
) -> str:
“””
Récupère les posts d’un subreddit donné.

```
Args:
    subreddit: Nom du subreddit (sans r/)
    sort: Type de tri (hot, new, top, rising)
    limit: Nombre de posts à récupérer (max 100)
    time_filter: Filtre temporel pour 'top' (hour, day, week, month, year, all)

Returns:
    JSON avec la liste des posts
"""
endpoint = f"/r/{subreddit}/{sort}"
params = {
    "limit": min(limit, 100),
    "raw_json": 1
}

if sort == "top":
    params["t"] = time_filter

try:
    response = await make_reddit_request(endpoint, params)
    if not response:
        return json.dumps({"error": "Impossible de récupérer les posts"})
    
    posts = []
    for item in response["data"]["children"]:
        try:
            post = parse_reddit_post(item)
            posts.append(post.model_dump())
        except Exception as e:
            logger.warning(f"Erreur lors du parsing d'un post: {e}")
            continue
    
    return json.dumps({
        "subreddit": subreddit,
        "sort": sort,
        "count": len(posts),
        "posts": posts
    }, indent=2)

except Exception as e:
    logger.error(f"Erreur get_subreddit_posts: {e}")
    return json.dumps({"error": str(e)})
```

@mcp.tool()
async def get_post_comments(
subreddit: str,
post_id: str,
limit: int = 50,
sort: str = “best”
) -> str:
“””
Récupère les commentaires d’un post spécifique.

```
Args:
    subreddit: Nom du subreddit
    post_id: ID du post
    limit: Nombre de commentaires à récupérer
    sort: Type de tri (best, top, new, controversial)

Returns:
    JSON avec la liste des commentaires
"""
endpoint = f"/r/{subreddit}/comments/{post_id}"
params = {
    "limit": min(limit, 100),
    "sort": sort,
    "raw_json": 1
}

try:
    response = await make_reddit_request(endpoint, params)
    if not response or len(response) < 2:
        return json.dumps({"error": "Impossible de récupérer les commentaires"})
    
    # Le premier élément contient le post, le second les commentaires
    post_data = response[0]["data"]["children"][0] if response[0]["data"]["children"] else None
    comments_data = response[1]["data"]["children"] if len(response) > 1 else []
    
    post_info = None
    if post_data:
        try:
            post_info = parse_reddit_post(post_data).model_dump()
        except Exception as e:
            logger.warning(f"Erreur lors du parsing du post: {e}")
    
    comments = []
    for comment_item in comments_data:
        try:
            comment = parse_reddit_comment(comment_item)
            if comment:
                comments.append(comment.model_dump())
        except Exception as e:
            logger.warning(f"Erreur lors du parsing d'un commentaire: {e}")
            continue
    
    return json.dumps({
        "post": post_info,
        "comments_count": len(comments),
        "comments": comments
    }, indent=2)

except Exception as e:
    logger.error(f"Erreur get_post_comments: {e}")
    return json.dumps({"error": str(e)})
```

@mcp.tool()
async def search_reddit(
query: str,
subreddit: Optional[str] = None,
sort: str = “relevance”,
time_filter: str = “all”,
limit: int = 25
) -> str:
“””
Recherche des posts sur Reddit.

```
Args:
    query: Terme de recherche
    subreddit: Subreddit spécifique (optionnel)
    sort: Type de tri (relevance, hot, top, new, comments)
    time_filter: Filtre temporel (hour, day, week, month, year, all)
    limit: Nombre de résultats à récupérer

Returns:
    JSON avec les résultats de recherche
"""
if subreddit:
    endpoint = f"/r/{subreddit}/search"
else:
    endpoint = "/search"

params = {
    "q": query,
    "sort": sort,
    "t": time_filter,
    "limit": min(limit, 100),
    "raw_json": 1
}

if subreddit:
    params["restrict_sr"] = "true"

try:
    response = await make_reddit_request(endpoint, params)
    if not response:
        return json.dumps({"error": "Impossible d'effectuer la recherche"})
    
    posts = []
    for item in response["data"]["children"]:
        try:
            post = parse_reddit_post(item)
            posts.append(post.model_dump())
        except Exception as e:
            logger.warning(f"Erreur lors du parsing d'un résultat: {e}")
            continue
    
    return json.dumps({
        "query": query,
        "subreddit": subreddit,
        "sort": sort,
        "time_filter": time_filter,
        "count": len(posts),
        "results": posts
    }, indent=2)

except Exception as e:
    logger.error(f"Erreur search_reddit: {e}")
    return json.dumps({"error": str(e)})
```

@mcp.tool()
async def get_subreddit_info(subreddit: str) -> str:
“””
Récupère les informations d’un subreddit.

```
Args:
    subreddit: Nom du subreddit

Returns:
    JSON avec les informations du subreddit
"""
endpoint = f"/r/{subreddit}/about"

try:
    response = await make_reddit_request(endpoint)
    if not response:
        return json.dumps({"error": "Impossible de récupérer les informations du subreddit"})
    
    data = response["data"]
    info = {
        "name": data["display_name"],
        "title": data["title"],
        "description": data["public_description"],
        "subscribers": data["subscribers"],
        "active_users": data.get("active_user_count", 0),
        "created_utc": data["created_utc"],
        "over18": data["over18"],
        "type": data["subreddit_type"],
        "lang": data.get("lang", ""),
        "url": data["url"]
    }
    
    return json.dumps(info, indent=2)

except Exception as e:
    logger.error(f"Erreur get_subreddit_info: {e}")
    return json.dumps({"error": str(e)})
```

@mcp.tool()
async def get_popular_subreddits(limit: int = 25) -> str:
“””
Récupère la liste des subreddits populaires.

```
Args:
    limit: Nombre de subreddits à récupérer

Returns:
    JSON avec la liste des subreddits populaires
"""
endpoint = "/subreddits/popular"
params = {
    "limit": min(limit, 100),
    "raw_json": 1
}

try:
    response = await make_reddit_request(endpoint, params)
    if not response:
        return json.dumps({"error": "Impossible de récupérer les subreddits populaires"})
    
    subreddits = []
    for item in response["data"]["children"]:
        data = item["data"]
        subreddit_info = {
            "name": data["display_name"],
            "title": data["title"],
            "subscribers": data["subscribers"],
            "active_users": data.get("active_user_count", 0),
            "description": data["public_description"][:200] + "..." if len(data["public_description"]) > 200 else data["public_description"],
            "over18": data["over18"],
            "url": data["url"]
        }
        subreddits.append(subreddit_info)
    
    return json.dumps({
        "count": len(subreddits),
        "subreddits": subreddits
    }, indent=2)

except Exception as e:
    logger.error(f"Erreur get_popular_subreddits: {e}")
    return json.dumps({"error": str(e)})
```

if **name** == “**main**”:
# Vérifier la configuration
if not config.client_id or not config.client_secret:
print(“ERREUR: Veuillez définir les variables d’environnement:”)
print(”- REDDIT_CLIENT_ID”)
print(”- REDDIT_CLIENT_SECRET”)
print(”- REDDIT_USER_AGENT (optionnel)”)
print(”\nPour obtenir ces identifiants:”)
print(“1. Allez sur https://www.reddit.com/prefs/apps”)
print(“2. Créez une nouvelle application”)
print(“3. Choisissez ‘script’ comme type d’application”)
exit(1)

```
print("Démarrage du serveur MCP Reddit...")
print(f"User Agent: {config.user_agent}")
mcp.run()
```