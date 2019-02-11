import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from hackernews_app.models import Article


def fetch_articles():
    # Just for development process
    # TODO: Remove this line after development
    Article.objects.all().delete()

    articles = []
    for page_num in range(1, 4):
        url = 'https://news.ycombinator.com/?p={page_num}'.format(page_num=str(page_num))
        request = urllib.request.Request(url)

        page = urllib.request.urlopen(request)
        soup = BeautifulSoup(page, 'html.parser')
        stories = soup.find('table', {'class': 'itemlist'}).findAll('tr')

        parsed_stories = []
        for story in stories:
            # Ignore all the TR tags which does not contains required fields
            if not (story.has_attr('class') and (story['class'][0] in ['spacer', 'morespace', 'morelink'])):
                parsed_stories.append(story)

        # In total N article's info is divided among N*2 tags, so grouping TRs
        # To form single article 
        parsed_stories = [parsed_stories[x:x+2] for x in range(0, len(parsed_stories), 2)]
        # Required Fields: Title, Url, No Of Comments, No Of Votes, Post Date

        for story in parsed_stories:
            data = {}
            for tr in story:
                if (tr.has_attr('class') and (tr['class'][0] == 'athing')):
                    title = tr.find('a', {'class': 'storylink'}).text
                    url = tr.find('a', {'class': 'storylink'})['href']
                    tag_id = tr.get('id')
                    hackernews_url = 'https://news.ycombinator.com/item?id={tag_id}'.format(tag_id=tag_id)

                    data['title'] = title
                    data['url'] = url
                    data['hackernews_url'] = hackernews_url
                    data['post_id'] = tag_id

                if tr.findAll('span', {'class': 'score'}):
                    upvotes = tr.find('span', {'class': 'score'}).text
                    data['upvotes'] = upvotes

                if tr.findAll('span', {'class': 'age'}):
                    post_hours_string = tr.find('span', {'class': 'age'}).text
                    if post_hours_string:
                        post_hour = int(''.join(filter(str.isdigit, post_hours_string)))
                        post_timestamp = datetime.now() - timedelta(hours=post_hour)
                        data['posted_on'] = post_timestamp
                    else:
                        data['posted_on'] = 'NA'
                    comment_string = tr.findAll('a', {'href':'item?id={}'.format(tag_id)})

                    if comment_string:
                        try:
                            comments = ''.join(filter(str.isdigit, comment_string[1].text))
                            data['comments'] = comments
                        except IndexError:
                            pass
                    else:
                        data['comments'] = 'NA'

            if data:
                articles.append(data)
                articles_list = Article.objects.all()
                if data.get('post_id') in [article.post_id for article in articles_list]:
                    # post is already present in our db
                    aritcle = Article.objects.filter(post_id=data['post_id'])
                    if aritcle:
                        article = Article(comments=data['comments'], upvotes=data['upvotes'])
                else:
                    article = Article(**data)
                article.save()

    print(articles)
