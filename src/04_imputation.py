def enrich_row(row, context_table=None):
    # Compléter avec ce qu'on a pu extraire des commentaires, images
    # context_table: table d'autres posts déjà traités pour imputation croisée
    if pd.isna(row['brand']) or pd.isna(row['model']) or pd.isna(row['year']):
        entities = extract_entities([row['body']] + [c['body'] for c in row.get('comments', [])])
        for key in ['brand', 'model', 'year']:
            if pd.isna(row[key]) and entities[key]:
                row[key] = entities[key]
    # Possible: enrichir à partir d'un contexte global/context_table
    # ... (complétion avancée à partir de context_table)
    return row