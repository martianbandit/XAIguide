import praw
import time

REDDIT_CLIENT_ID = 'VOTRE_CLIENT_ID'
REDDIT_SECRET = 'VOTRE_SECRET'
REDDIT_AGENT = 'pipeline-mecano-v1'
REQS_PER_MIN = 60

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET, user_agent=REDDIT_AGENT)

def reddit_fetch_post(url):
    try:
        submission = reddit.submission(url=url)
        post = {
            'title': submission.title,
            'body': submission.selftext,
            'created_utc': submission.created_utc,
            'flair': getattr(submission, 'link_flair_text', None),
            'images': [x['url'] for x in getattr(submission, 'preview', {}).get('images', [])]
        }
        return post, submission
    except Exception as e:
        print(f"Erreur Reddit sur {url}: {e}")
        return None, None

def reddit_fetch_comments(submission, min_score=1, min_len=30):
    if submission is None:
        return []
    submission.comments.replace_more(limit=0)
    comments = []
    for c in submission.comments.list():
        if len(getattr(c, 'body', '')) >= min_len and c.score >= min_score:
            comments.append({'body': c.body, 'score': c.score, 'author': str(c.author)})
    return comments

def batch_reddit_fetch(urls, sleep_per_req=1.1):
    all_posts = []
    for i, url in enumerate(urls):
        post, submission = reddit_fetch_post(url)
        time.sleep(sleep_per_req)  # throttle!
        comments = reddit_fetch_comments(submission)
        all_posts.append({'url_post': url, **(post or {}), 'comments': comments})
        if (i+1) % REQS_PER_MIN == 0:
            print("Pause pour éviter le rate-limit Reddit…")
            time.sleep(60)
    return all_posts