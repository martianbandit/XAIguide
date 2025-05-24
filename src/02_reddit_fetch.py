import praw
import time
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

REQS_PER_MIN = 60

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def throttle(i):
    if (i + 1) % REQS_PER_MIN == 0:
        time.sleep(65)
    else:
        time.sleep(1.1)

def reddit_fetch_post(url):
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
        return {
            'url_post': url,
            'title': submission.title,
            'body': submission.selftext,
            'flair': getattr(submission, 'link_flair_text', None),
            'created_utc': submission.created_utc,
            'comments': comments,
            'images': images
        }
    except Exception as e:
        print(f"Erreur Reddit sur {url}: {e}")
        return {'url_post': url, 'error': str(e)}

def enrich_df_with_reddit(df):
    enriched = []
    for i, row in df.iterrows():
        data = reddit_fetch_post(row['url_post'])
        throttle(i)
        combined = row.to_dict()
        combined.update(data)
        enriched.append(combined)
    return enriched