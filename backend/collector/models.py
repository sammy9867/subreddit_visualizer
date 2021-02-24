from django.db import models

# Add description for Submissions and Comments in the 2nd phase
class Subreddit(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    display_name = models.CharField(max_length=30, blank=False, default='')
    title =  models.CharField(max_length=100, blank=False, default='')

class Redditor(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50, blank=False, default='')

class Submission(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    redditor = models.ForeignKey(Redditor, on_delete=models.CASCADE)
    karma = models.IntegerField()
    upvote_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    num_comments = models.IntegerField()
    created_utc = models.DateTimeField()

class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    redditor = models.ForeignKey(Redditor, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    karma = models.IntegerField()
    created_utc = models.DateTimeField()