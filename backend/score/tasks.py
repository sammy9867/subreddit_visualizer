from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime, timedelta

from celery import shared_task

from django.utils import timezone
from django.conf import settings

from score.models import WeeklyRedditorScore
from collector.models import Submission, Comment, Subreddit
from api_clients.reddit import RedditAPIClient


@shared_task
def get_subreddits_every_monday_task():
    submission_limit = settings.SUBMISSION_LIMIT
    comment_limit = settings.COMMENT_LIMIT
    end_day = datetime.now(tz=timezone.utc)
    start_day = end_day - timedelta(days=7)
    subreddits = [
        "Bitcoin",
        "wallstreetbets",
        "fitness",
        "sports",
        "politics",
        "movies",
        "news",
    ]
    reddit_client = RedditAPIClient()
    reddit_client.get_subreddits(
        subreddits,
        int(submission_limit),
        int(comment_limit),
        start_day.date(),
        end_day.date(),
    )

    # Save Weekly Score Every Monday
    for subreddit_name in subreddits:
        compute_score(subreddit_name, start_day, end_day, "SUB")
        compute_score(subreddit_name, start_day, end_day, "COM")


def compute_score(subreddit_name, start_day, end_day, score_type):
    top_counter = 1
    week_number = start_day.isocalendar()[1]
    try:
        subreddit = Subreddit.objects.get(display_name=subreddit_name)
    except Subreddit.DoesNotExist:
        return  # Handle Error later

    if score_type == "SUB":
        top_submissions = []
        submissions = Submission.objects.filter(
            subreddit_id=subreddit.id, created_utc__range=[start_day, end_day]
        )
        for submission in submissions:
            if top_counter > 5:
                break
            score = float(
                submission.karma * submission.upvote_ratio
            )  # float(submission.num_comments/2)
            top_submissions.append((top_counter, score, submission))
            top_counter += 1
        save_weekly_score(top_submissions, score_type, week_number, start_day)
    elif score_type == "COM":
        top_comments = []
        comments = Comment.objects.filter(
            subreddit_id=subreddit.id, created_utc__range=[start_day, end_day]
        )
        for comment in comments:
            if top_counter > 5:
                break
            score = float(comment.karma)
            top_comments.append((top_counter, score, comment))
            top_counter += 1
        save_weekly_score(top_comments, score_type, week_number, start_day)


def save_weekly_score(top_list, score_type, week_number, start_day):
    print("Score Type", score_type)
    print("Week Number", week_number)
    for rank, score, top in top_list:
        weekly_score_saved = WeeklyRedditorScore(
            subreddit_id=top.subreddit.id,
            redditor_id=top.redditor.id,
            score_type=score_type,
            score=score,
            rank=rank,
            week_number=week_number,
            created_utc=start_day,
        )
        weekly_score_saved.save()
