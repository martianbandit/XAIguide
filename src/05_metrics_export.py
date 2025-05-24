import json

def export_jsonl(df, path, mode='full'):
    with open(path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            if mode == 'full':
                f.write(json.dumps(row.to_dict(), ensure_ascii=False) + '\\n')
            elif mode == 'concise':
                f.write(json.dumps({
                    'system_prompt': 'Diagnostique comme un mécanicien professionnel.',
                    'post': row.get('body', ''),
                    'consensus': row.get('consensus', '')
                }, ensure_ascii=False) + '\\n')
