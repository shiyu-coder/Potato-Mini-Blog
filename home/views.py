from django.shortcuts import render
from article.models import ArticlePost


# Create your views here.
def home_page(request):
    return render(request, 'index.html')

