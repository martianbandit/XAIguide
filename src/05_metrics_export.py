import json

def completeness_score(row):
    needed = ['brand', 'model', 'year', 'problem', 'comments']
    filled = sum([row.get(k) not in [None, '', pd.NA] for k in needed])
    return filled / len(needed)

def export_jsonl(posts, path, mode='full'):
    with open(path, 'w', encoding='utf-8') as f:
        for post in posts:
            if mode == 'full':
                f.write(json.dumps(post, ensure_ascii=False) + '\\n')
            elif mode == 'concise':
                out = {
                    'system_prompt': 'Diagnostique comme un mécanicien pro.',
                    'post': post.get('body'),
                    'consensus': post.get('consensus', '')
                }
                f.write(json.dumps(out, ensure_ascii=False) + '\\n')