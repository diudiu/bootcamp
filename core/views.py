import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect

from feeds.views import FEEDS_NUM_PAGES, feeds
from feeds.models import Feed
from articles.models import Article, ArticleComment
from questions.models import Question, Answer
from activities.models import Activity

def home(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        return render(request, 'core/cover.html')


@login_required
def network(requst):
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = requst.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(requst, 'core/network.html', {'users': users})


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id

    feeds_count = Feed.objects.filter(user=page_user).count()
    article_count = Article.objects.filter(create_user=page_user).count()
    article_comment_count = ArticleComment.objects.filter(
        user=page_user).count()
    question_count = Question.objects.filter(user=page_user).count()
    answer_count = Answer.objects.filter(user=page_user).count()
    activity_count = Activity.objects.filter(user=page_user).count()
    # messages_count =
    data, datepoints = Activity.daily_activity(page_user)
    data = {
        'page_user': page_user,
        'feeds_count': feeds_count,
        'article_count': article_count,
        'article_comment_count': article_comment_count,
        'question_count': question_count,
        'global_interactions': activity_count + article_comment_count + answer_count, # + messages_count,
        'answer_count': answer_count,
        'bar_data': [
            feeds_count, article_count, article_comment_count, question_count,
            answer_count, activity_count
        ],
        'bar_labels': json.dumps('["Feeds", "Articles", "Comments", "Questions", "Answers", "Activities"]'),
        'line_labels': datepoints,
        'line_data': data,
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1
    }
    return render(request, 'core/profile.html', data)