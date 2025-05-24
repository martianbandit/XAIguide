import praw
import time
import logging

REDDIT_CLIENT_ID = 'VOTRE_ID'
REDDIT_SECRET = 'VOTRE_SECRET'
REDDIT_AGENT = 'reddit_mecano_pipeline'

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent=REDDIT_AGENT)

RATE_LIMIT = 60  # Reddit = 60 requêtes / min

def throttle(i):
    if (i + 1) % RATE_LIMIT == 0:
        print("Quota atteint. Pause de sécurité...")
        time.sleep(65)
    else:
        time.sleep(1.1)

def fetch_reddit_data(urls):
    data = []
    for i, url in enumerate(urls):
        try:
            submission = reddit.submission(url=url)
            submission.comments.replace_more(limit=0)
            comments = [
                {'body': c.body, 'score': c.score, 'author': str(c.author)}
                for c in submission.comments.list()
                if len(c.body) > 30 and c.score >= 1
            ]
            images = []
            if hasattr(submission, 'preview'):
                images = [img['source']['url'] for img in submission.preview.get('images', [])]
            data.append({
                'url_post': url,
                'title': submission.title,
                'body': submission.selftext,
                'flair': getattr(submission, 'link_flair_text', None),
                'created_utc': submission.created_utc,
                'comments': comments,
                'images': images
            })
        except Exception as e:
            logging.error(f"Erreur sur {url}: {e}")
            data.append({'url_post': url, 'error': str(e)})
        throttle(i)
    return data
