# hackernews clone

This is a clone of hackernews(https://news.ycombinator.com)

Checkout https://ycombinator-news.herokuapp.com/

## How To Run This project

1. Clone this repo
2. Install all the requirements.
3. Set Following ENV Varibales, [DB_NAME, DB_HOST, DB_PASSWORD, DB_USER, DB_PORT] and make sure the value you select
for your env variable should be valid
4. python manage.py runserver
5. go to https://ycombinator-news.herokuapp.com/fetch_stories to trigger the scraper script which updates the database

## Features
1. Check hackernews_app/scraper.py for scraper script
2. hackernews_app/views.py contains the logic for login, register, mark articles as read, delete, fetch all read articles etc.


   
