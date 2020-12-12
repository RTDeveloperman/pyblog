from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import  datetime

def validate_file_extension(value):
    import  os
    from django.core.exceptions import ValidationError
    ext=os.path.splitext(value.name)[1]
    valid_extention=['.jpg','.png']
    if not ext.lower() in valid_extention:
        raise ValidationError('Unsupported File Extension')

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    avatar=models.FileField(upload_to='files/user_avatar/', null=True, blank=True,validators=[validate_file_extension])
    description=models.CharField(max_length=512, null=False, blank=False)

class Article(models.Model):
    title=models.CharField(max_length=124,null=False, blank= False)
    cover=models.FileField(upload_to='files/article_cover/', null=False, blank= False,validators=[validate_file_extension])
    content=RichTextField()
    created_at=models.DateTimeField(default=datetime.now(),blank=False)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)#Category dakhel single cotaion hast chon class category paeen tar tarif shode
    author=models.ForeignKey(UserProfile,on_delete=models.CASCADE)# agar mikhaym nevisande pak shod maghalatesh pak nashe on delete ro bayad hazf kard
    def __str__(self):
       return self.title
class Category(models.Model):
    title=models.CharField(max_length=128,null=False, blank= False)
    cover=models.FileField(upload_to='files/category_Cover/',null=False, blank=False,validators=[validate_file_extension])
    def __str__(self):
        return self.title

