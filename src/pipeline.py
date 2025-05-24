def compile_lexicon(posts):
    lex = Counter()
    for post in posts:
        lex.update(extract_vocab([post.get('body', '')] + [c['body'] for c in post.get('comments', [])]))
    return lex

def export_lexicon(lex, path):
    with open(path, 'w', encoding='utf-8') as f:
        for word, count in lex.most_common():
            f.write(f\"{word},{count}\\n\")

def export_images(posts, path):
    with open(path, 'w', encoding='utf-8') as f:
        for post in posts:
            for img_url in post.get('images', []):
                f.write(json.dumps({'url_post': post['url_post'], 'img_url': img_url}) + '\\n')