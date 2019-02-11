from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    """Article Model
    """
    post_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    hackernews_url = models.CharField(max_length=255)
    upvotes = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    posted_on = models.DateTimeField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'api_articles'


class UserReadingHistory(models.Model):
    """User Reading History Model
    """
    user = models.ForeignKey(User, models.CASCADE)
    article = models.ForeignKey(Article, models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_user_reading_history'


class ArticleDeletedByUser(models.Model):
    """User Reading History Model
    """
    user = models.ForeignKey(User, models.CASCADE)
    article = models.ForeignKey(Article, models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_user_article_deletion_history'