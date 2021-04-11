from django import forms
from .models import ArticlePost
from mdeditor.fields import MDTextFormField


class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        fields = ('title', 'body', 'tags', 'avatar')


# class MDEditorModleForm(forms.ModelForm):
#     class Meta:
#         model = ArticlePost
#         fields = '__all__'
