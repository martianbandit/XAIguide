def impute_from_context(row, full_dataset=None):
    ents = row.get('entities', {})
    for key in ['brand', 'model', 'year']:
        if not row.get(key) and ents.get(key):
            row[key] = ents[key]
        # Recherche dans full_dataset si pas trouvé
        if not row.get(key) and full_dataset is not None:
            match = full_dataset[(full_dataset['url_post'] != row['url_post']) & (full_dataset[key].notna())]
            if not match.empty:
                row[key] = match[key].mode().iloc[0]
    return row
