from django.urls import path
from django.conf.urls import url

from hackernews_app import views

# SET THE NAMESPACE!
app_name = 'news'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('mark_as_read/<int:id>/', views.mark_as_read, name='mark_as_read'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('my_articles/', views.user_articles, name='user_articles')
]