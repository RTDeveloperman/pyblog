from django.shortcuts import render
from django.template.defaultfilters import title
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from .models import *
from . import  serializers
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

class AllArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            all_articles=Article.objects.all().order_by('-created_at') [:5]
            data= []
            for article in all_articles:
                data.append({
                    "title":article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote,

                })
            return Response({'data':data},status=status.HTTP_200_OK)
        except:
            return Response({'status':'Internal server Error!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SingleArticleAPIView(APIView):
    def get(self,request,format=None):
        try:
            article_title=request.GET['article_title']
            article=Article.objects.filter(title__contains=article_title)
            serialized_data=serializers.SingleArticleSerializers(article,many=True)
            data=serialized_data.data
            return Response({'data':data},status=status.HTTP_200_OK)
        except:
            return Response({'status' : 'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)