from rest_framework import serializers

from blog.models import UserProfile


class SingleArticleSerializers(serializers.Serializer):
    title=serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=128)
    cover=serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=256)
    content=serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=2048)
    created_at=serializers.DateTimeField(required=True,allow_null=False)
class SearchArticleSerializers(serializers.Serializer):
    title = serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=128)
    cover = serializers.ImageField(required=True )
    content = serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=2048)
    created_at=serializers.DateTimeField(required=True,allow_null=False)
    category = serializers.CharField(required=True,allow_null=False,allow_blank=False,max_length=128)
    author = serializers.SerializerMethodField('Get_Auther_Details')
    promote = serializers.BooleanField(required=False)
    def Get_Auther_Details(self,obj):
        return obj.author.user.first_name+' ' + obj.author.user.last_name



class SubmitArticleSerializers(serializers.Serializer):
    title=serializers.CharField(required=True,allow_blank=False,allow_null=False,max_length=120)
    cover=serializers.FileField(required=True,allow_null=False,allow_empty_file=False)
    content=serializers.CharField(required=True,allow_blank=False,allow_null=False,max_length=2048)
    #created_at=serializers.DateTimeField(required=True,allow_null=False)
    category_id=serializers.IntegerField(required=True,allow_null=False)
    author_id=serializers.IntegerField(required=True,allow_null=False)
    promote=serializers.IntegerField(required=True,allow_null=False)

class UpdateCoverArticleSerializer(serializers.Serializer):
    article_id=serializers.IntegerField(required=True,allow_null=False)
    cover=serializers.FileField(required=True,allow_null=False,allow_empty_file=False)


class DeleteArticleSerializer(serializers.Serializer):
    article_id=serializers.IntegerField(required=True,allow_null=False)
