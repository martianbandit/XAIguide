from collections import Counter
import re
import spacy

nlp = spacy.load('fr_core_news_sm')

def extract_entities(texts):
    ent = {'brand': None, 'model': None, 'year': None}
    for txt in texts:
        doc = nlp(str(txt))
        for e in doc.ents:
            if e.label_ == 'ORG' and not ent['brand']:
                ent['brand'] = e.text
            elif e.label_ == 'PRODUCT' and not ent['model']:
                ent['model'] = e.text
            elif e.label_ == 'DATE' and not ent['year']:
                ent['year'] = e.text
    return ent

def extract_vocab(texts):
    words = []
    for t in texts:
        words.extend(re.findall(r'\\b\\w+\\b', t.lower()))
    return Counter(words)

def describe_images(image_urls):
    # Placeholder – à remplacer par BLIP2 ou Gemini API
    return [f'Image trouvée à {url} (description automatique à venir)' for url in image_urls]
