from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from . import forms
from .models import ArticlePost
import markdown
from django.contrib.auth.decorators import login_required
from django.views import View, generic
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from .models import ArticleColumn
from comment.forms import CommentForm
from userprofile.models import Profile
import numpy as np
from django.db.models.aggregates import Count


# Create your views here.
def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()
    latest_posts = article_list[:4]

    # 分类信息
    columns = ArticleColumn.objects.annotate(num_articles=Count('article'))
    # 获取所有标签
    tags = set()
    for article in article_list:
        for ta in article.tags.all():
            tags.add(ta)
    tags = list(tags)
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column != 'None' and column is not None and column != '':
        col_index = ArticleColumn.objects.get(title=column).id
        article_list = article_list.filter(column_id=col_index)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # print(len(article_list), len(articles))
    profile = []
    for article in articles:
        info = Profile.objects.get(user_id=article.author.id)
        can = True
        for old_info in profile:
            if old_info.avatar.url == info.avatar.url:
                can = False
        if can:
            profile.append(info)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'latest_posts': latest_posts,
        'profiles': profile,
        'columns': columns,
        'tags': tags,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }

    return render(request, 'blog.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = get_object_or_404(ArticlePost, id=id)
    pro = Profile.objects.get(user_id=article.author.id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 初始化查询集
    article_list = ArticlePost.objects.all()
    # 分类信息
    columns = ArticleColumn.objects.annotate(num_articles=Count('article'))
    # 获取所有标签
    tags = set()
    for arti in article_list:
        for tag in arti.tags.all():
            tags.add(tag)
    tags = list(tags)
    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    profile = []
    for arti in articles:
        info = Profile.objects.get(user_id=arti.author.id)
        can = True
        for old_info in profile:
            if old_info.avatar.url == info.avatar.url:
                can = False
        if can:
            profile.append(info)
    # # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body,
    #                                  extensions=[
    #                                      # 包含缩写、表格等常用扩展
    #                                      'markdown.extensions.extra',
    #                                      # 语法高亮扩展
    #                                      'markdown.extensions.codehilite',
    #                                      # 目录扩展
    #                                      'markdown.extensions.toc',
    #                                  ])

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 过滤出所有的id比当前文章小的文章
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    # 过滤出id大的文章
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')

    # 取出相邻前一篇文章
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    # 取出相邻后一篇文章
    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None
    # 新增了md.toc对象
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    # 需要传递给模板的对象
    context = {
        'article': article,
        'pro': pro,
        'toc': md.toc,
        'comments': comments,
        'comment_form': comment_form,
        'pre_article': pre_article,
        'next_article': next_article,
        'articles': articles,
        'profiles': profile,
        'columns': columns,
        'tags': tags,
    }

    # 载入模板，并返回context对象
    return render(request, 'post.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表格实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'create.html', context)


# class MDEditorModleForm(generic.CreateView):
#     form_class = forms.MDEditorModleForm
#     template_name = 'create.html'
#
#     def get_success_url(self):
#         return reverse('article:edit')


# 删文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body、brief 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.brief = request.POST['brief']
            # 新增的代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        # 将响应返回到模板中
        return render(request, 'update.html', context)


# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')

