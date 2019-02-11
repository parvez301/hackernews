from django.contrib import admin
from hackernews_app.models import Article, UserReadingHistory, ArticleDeletedByUser
# Register your models here.
admin.site.register(Article)
admin.site.register(UserReadingHistory)
admin.site.register(ArticleDeletedByUser)
