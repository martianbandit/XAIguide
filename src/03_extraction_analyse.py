import spacy
import re
from collections import Counter

# --- NER (marque, modèle, année, etc.) ---
nlp = spacy.load('fr_core_news_sm')

def extract_entities(texts):
    info = {'brand': None, 'model': None, 'year': None}
    for text in texts:
        doc = nlp(str(text))
        for ent in doc.ents:
            if ent.label_ == 'ORG' and not info['brand']:
                info['brand'] = ent.text
            elif ent.label_ == 'PRODUCT' and not info['model']:
                info['model'] = ent.text
            elif ent.label_ == 'DATE' and not info['year']:
                info['year'] = ent.text
    return info

# --- Lexique technique ---
def extract_vocab(all_texts):
    words = []
    for txt in all_texts:
        words += re.findall(r"\\b\\w+\\b", str(txt).lower())
    return Counter(words)

# --- (Optionnel) Description automatique d'image (modèle externe) ---
def describe_images(image_urls):
    # À intégrer: call BLIP2, Gemini Vision, etc.
    return ["Description automatique (à implémenter)" for _ in image_urls]