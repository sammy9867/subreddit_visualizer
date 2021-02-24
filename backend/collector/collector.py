import os
from datetime import datetime, timedelta

import praw
from dotenv import load_dotenv, find_dotenv

from django.utils import timezone
from collector.models import Subreddit, Submission, Comment, Redditor

# Loading .env file
load_dotenv(find_dotenv())

class SubredditCollector:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent=os.environ.get('REDDIT_USER_AGENT')
        )

    def get_subreddits(self, subreddits, submission_limit, comment_limit, start_day, end_day):
        for subreddit in subreddits:
            num_submissions = submission_limit
            validated_subreddit = self.reddit.subreddit(subreddit)
            if validated_subreddit is None:
                continue
            self.save_subreddit(validated_subreddit)
            for submission in validated_subreddit.top("week"):
                if submission is None or num_submissions <= 0:
                    continue
                if self.is_submission_saved(submission, start_day, end_day):
                    num_submissions -= 1
                    submission.comments.replace_more(limit=1)
                    num_comments = comment_limit
                    for comment in submission.comments.list():
                        if comment is None or num_comments <= 0:
                            break
                        if self.is_comment_saved(comment, submission.id, start_day, end_day):
                            num_comments -= 1
            
    def save_subreddit(self, subreddit):
        try:
            subreddit_saved = Subreddit.objects.get(pk=subreddit.id)
        except Subreddit.DoesNotExist:
            print("Subreddit", subreddit.display_name)
            subreddit_saved = Subreddit(
                id=subreddit.id, 
                display_name=subreddit.display_name, 
                title=subreddit.title
            )
            subreddit_saved.save()

    def is_redditor_saved(self, redditor):
        if redditor is None or not hasattr(redditor, 'id'):
            return False
        try:
            redditor_saved = Redditor.objects.get(pk=redditor.id)
        except Redditor.DoesNotExist:
            redditor_saved = Redditor(id=redditor.id, name=redditor.name)
            redditor_saved.save()
        return True

    def is_submission_saved(self, submission, start_day, end_day):
        if not self.is_redditor_saved(submission.author):
            return False
        try:
            submission_saved = Submission.objects.get(pk=submission.id)
        except Submission.DoesNotExist:
            created_utc = self.unix_timestamp_to_datetime(submission.created_utc)
            if created_utc.date() < start_day or created_utc.date() > end_day:
                return False
            print("Submission", submission.id, created_utc.date())
            submission_saved = Submission(
                id=submission.id,
                redditor_id=submission.author.id,
                subreddit_id=submission.subreddit.id,
                karma=submission.score,
                upvote_ratio=submission.upvote_ratio,
                num_comments=submission.num_comments,
                created_utc=created_utc
            )
            submission_saved.save()
        return True

    def is_comment_saved(self, comment, submission_id, start_day, end_day):
        if not self.is_redditor_saved(comment.author):
            return False
        try:
            comment_saved = Comment.objects.get(pk=comment.id)
        except Comment.DoesNotExist:
            created_utc = self.unix_timestamp_to_datetime(comment.created_utc)
            print("Comment", comment.id, created_utc.date())
            comment_saved = Comment(
                id=comment.id,
                redditor_id=comment.author.id,
                subreddit_id=comment.subreddit.id,
                submission_id=submission_id,
                karma=comment.score,
                created_utc=created_utc
            )
            comment_saved.save()
        return True

    def unix_timestamp_to_datetime(self, unix_timestamp):
        if unix_timestamp != None:
            dt = datetime.fromtimestamp(int(unix_timestamp))
            return timezone.make_aware(dt, timezone.utc)
        return None