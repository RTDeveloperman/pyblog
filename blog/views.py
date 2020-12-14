from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

class IndexPage(TemplateView):
    #template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9]
        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })

        all_promote_article=Article.objects.filter(promote=True)
        promte_data= []
        for promote_article in all_promote_article:
            promte_data.append({
                'title': promote_article.title,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'category': promote_article.category.title,
                'created_at': promote_article.created_at.date(),
                'avatar':promote_article.author.avatar.url if promote_article.author.avatar else None,
                'author':promote_article.author.user.first_name+' '+promote_article.author.user.last_name,
            })

            context = {
                'article_data': article_data,
                'all_promote_article':promte_data,
            }
        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'
    #def get(self, request, *args, **kwargs):
     #   return render(request,'page-contact.html')

