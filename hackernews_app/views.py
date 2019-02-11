from django.shortcuts import render
from django.http import HttpResponse

from hackernews_app.scraper import fetch_articles
from hackernews_app.models import Article, UserReadingHistory, ArticleDeletedByUser

from hackernews_app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def fetch_stories(request):
    """I've exposed the scraper script
    using one endpoint, we just need to call
    /fetch_stories/ and it will updates the DB
    """
    fetch_articles()
    return HttpResponse('Stories has been updated in the database')


def index(request):
    articles = {}
    if request.user.is_authenticated:
        user = request.user
        user_articles = UserReadingHistory.objects.filter(user=user)
        articles_deleted_by_user = ArticleDeletedByUser.objects.filter(user=user)
        articles_to_exculde = user_articles.union(articles_deleted_by_user)
        articles = Article.objects.filter(active=1).exclude(id__in=[i.article_id for i in articles_to_exculde]).order_by('-posted_on')
    return render(request, 'hackernews_app/index.html', {'articles': articles})


@login_required
def user_logout(request):
    """Logout Method
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """Method for user registration
    """
    if request.user.is_authenticated:
        # If user is already authenticate, take user to index page
        return HttpResponseRedirect(reverse('index'))

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'hackernews_app/registration.html',
                          {'user_form':user_form,
                           'registered':registered})


def user_login(request):
    """This function contains the login
    functionalities
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'hackernews_app/login.html', {})


def mark_as_read(request, id):
    """This method contains the logic to 
    mark stories as read"""
    if request.user.is_authenticated:
        user = request.user
        article = Article.objects.get(id=id)
        UserReadingHistory(user=user, article=article).save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('User Authentication Failed, Kindly Login again')

def delete(request, id):
    if request.user.is_authenticated:
        user = request.user
        article = Article.objects.get(id=id)
        ArticleDeletedByUser(user=user, article=article).save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('User Authentication Failed, Kindly Login again')

def user_articles(request):
    """This method returns the articles
    which user has marked as read
    """
    if request.user.is_authenticated:
        user_articles = UserReadingHistory.objects.filter(user=request.user)
        articles = Article.objects.filter(id__in=[i.article_id for i in user_articles]) 
        return render(request, 'hackernews_app/index.html', {'articles': articles})
    else:
        return HttpResponse('User Authentication Failed, Kindly Login again')
