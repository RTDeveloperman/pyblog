from django.shortcuts import render
from django.template.defaultfilters import title
from django.views.generic import TemplateView
from rest_framework.generics import UpdateAPIView
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


class SearchArticlePIView(APIView):
    def get(self,request,format=None):
        try:
            from django.db.models import Q#baraye anjame query haye pishrafte
            query=request.GET['query']
            article= Article.objects.filter(Q(content__icontains=query))
            data=[]
            serializerdata=serializers.SearchArticleSerializers(article,many=True)
            data=serializerdata.data
            return Response({'data':data},status=status.HTTP_200_OK)
        except:
            return Response({'data':'Internal server Error!:('},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitArticlePIView (APIView):
    def post(self,request,format=None):
        try:
            serializer=serializers.SubmitArticleSerializers(data=request.data)
            if serializer.is_valid():
                title=serializer.data.get('title')
                cover= request.FILES['cover']
                content= serializer.data.get('content')
                category_id=serializer.data.get('category_id')
                author_id= serializer.data.get('author_id')
                promote= serializer.data.get('promote')
            else:
                return Response({'Statuse':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)

            user=User.objects.get(id=author_id)
            author=UserProfile.objects.get(user=user)
            category=Category.objects.get(id=category_id)

            article=Article()
            article.title=title
            article.cover=cover
            article.content=content
            article.author=author
            article.category=category
            article.promote=promote
            article.save()
            return Response({'status':'O.K'},status=status.HTTP_200_OK)
        except:
            return Response({'data': 'Internal server Error!:`('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateArticlePIView(UpdateAPIView):
    def post(self,request,format=None):
        try:
            serializer=serializers.UpdateCoverArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id=serializer.data.get('article_id')
                cover= request.FILES['cover']
                Article.objects.filter(id=article_id).update(cover=cover)
                return Response({'data': 'Update O.k .'}, status=status.HTTP_200_OK)


            else:
                return Response({'data': 'Bad Requiest!'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'data': 'Internal server Error!:`('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticlePIView (APIView):
    def post(self,request,format=None):
        try:
            serializer=serializers.DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id=serializer.data.get('article_id')
                Article.objects.filter(id=article_id).delete()
                return Response({'data': 'O.k'}, status=status.HTTP_200_OK)

            else:
                return Response({'data': 'Bad Requiest!'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'data': 'Internal server Error!:`('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
