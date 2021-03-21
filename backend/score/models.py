from django.db import models
from reddit.models import Redditor, Subreddit

# Top 5 submitters and commenters per week
class WeeklyRedditorScore(models.Model):
    class ScoreType(models.TextChoices):
        SUBMISSION = "SUB", "Submission"
        COMMENT = "COM", "Comment"

    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    redditor = models.ForeignKey(Redditor, on_delete=models.CASCADE)
    score_type = models.CharField(max_length=3, choices=ScoreType.choices, blank=False)
    score = models.DecimalField(max_digits=10, decimal_places=2)
    rank = models.PositiveIntegerField()
    week_number = models.PositiveIntegerField()
    created_utc = models.DateTimeField()

    def __str__(self):
        return f"Score type: {self.score_type} with rank: {self.rank}"
