from django.shortcuts import render
from article.models import ArticlePost, ArticleColumn
import numpy as np
from django.db.models.aggregates import Count
from django.core.paginator import Paginator
from django.db.models import Q
from userprofile.models import Profile
from django.contrib.auth.models import User


# Create your views here.
def home_page(request):

    # 初始化查询集
    article_list = ArticlePost.objects.all()
    article_most_view = article_list.order_by('-total_views')[:3]

    # 获取当前用户总数
    user_num = len(User.objects.all())

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # paginator_view = Paginator(article_most_view, 3)
    # page_view = request.GET.get('page')
    # articles_view = paginator_view.get_page(page_view)

    profile = []
    profile_view = []
    for article in articles:
        info = Profile.objects.get(user_id=article.author.id)
        can = True
        for old_info in profile:
            if old_info.avatar.url == info.avatar.url:
                can = False
        if can:
            profile.append(info)

    for article in article_most_view:
        info = Profile.objects.get(user_id=article.author.id)
        can = True
        for old_info in profile_view:
            if old_info.avatar.url == info.avatar.url:
                can = False
        if can:
            profile_view.append(info)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'articles_view': article_most_view,
        'profiles': profile,
        'profiles_view': profile_view,
        'user_num': str(user_num),
    }

    return render(request, 'index.html', context)

