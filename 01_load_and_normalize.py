import pandas as pd

COLS_STD = [
    'url_post', 'problem', 'brand', 'model', 'year', 'vehicle_type',
    'TOUT LES COMMENTAIRES', 'images', 'mileage'
]

def load_and_normalize(filepath):
    df = pd.read_csv(filepath)
    # Normaliser les noms de colonnes (multi-langues, variantes)
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for col in COLS_STD:
        if col not in df.columns:
            # Ajoute la colonne manquante (NaN)
            df[col] = pd.NA
    # Réordonne
    df = df[COLS_STD + [c for c in df.columns if c not in COLS_STD]]
    return df