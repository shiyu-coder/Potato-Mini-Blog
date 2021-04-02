from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
import markdown


# Create your views here.
def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    # return render(request, 'article/list.html', context)
    return render(request, 'blog.html', context)


def article_detail(request, id):
    # 取出文章
    article = ArticlePost.objects.get(id=id)
    # 对markdown语法渲染成html格式
    article.body = markdown.markdown(
        article.body,
        extensions=[
            # 缩写表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
        ]
    )
    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回对象
    return render(request, 'post.html', context)


