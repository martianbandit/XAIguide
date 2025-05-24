# Reddit Mécano Pipeline

Pipeline open source pour l’extraction, l’analyse et l’enrichissement de discussions Reddit sur la mécanique (notamment diesel et véhicules lourds).

## Fonctionnalités principales
- Ingestion de données Reddit (posts + commentaires)
- Extraction d’entités mécaniques : marque, modèle, année, panne, pièces
- Description automatique d’images techniques
- Génération de consensus communautaires
- Export .jsonl (complet & concis), lexique, métriques, tableau d’images

## Installation
```bash
git clone https://github.com/votreutilisateur/reddit-mecano-pipeline.git
cd reddit-mecano-pipeline
pip install -r requirements.txt