from django.db import models

# Create your models here.

class SecureInfo(models.Model):
    accessToken = models.CharField(max_length=255)
    refreshToken = models.CharField(max_length=255)

class UserInfo(models.Model):
    openid = models.CharField(max_length=255, primary_key=True)
    headimgurl = models.CharField(max_length=512)
    nickname = models.CharField(max_length=255)
    unionid = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    sex = models.IntegerField(default=-1)

class CommentInfo(models.Model):
    dayid = models.CharField(max_length=255)
    openid = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    created = models.CharField(max_length=255)
