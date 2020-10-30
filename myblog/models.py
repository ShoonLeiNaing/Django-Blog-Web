from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.conf import settings


class Post(models.Model):
    title=models.CharField(max_length=256,validators=[MinLengthValidator(10,"Title must be greater than 10 characters")])
    context=models.TextField()
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="post_owner")
    favorite=models.ManyToManyField(settings.AUTH_USER_MODEL,through="Fav",related_name="favorite_posts")
    picture=models.BinaryField(null=True,blank=True,editable=True)
    comments=models.ManyToManyField(settings.AUTH_USER_MODEL,through="Comment",related_name="post_comment")
    content_type=models.CharField(max_length=256,null=True,blank=True,editable=True,help_text="The MIMEType of the file")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text=models.TextField(max_length=512,validators=[MinLengthValidator(2,"Comments must be greater than 2 characters")])
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Fav(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together=('post','user')

    def __str__(self):
        return '%s likes %s'%(self.user.username,self.post.title)
