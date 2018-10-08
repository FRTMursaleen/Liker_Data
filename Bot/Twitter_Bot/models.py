# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
from django.db import models
from django.core.validators import MinValueValidator
from django.core import validators
from django.contrib.auth.models import User

# Create your models here.
#
class Accounts_Data(models.Model):
    user = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    account = models.IntegerField(primary_key=True, )
    Access_token = models.CharField(null= False, max_length=100 , unique=True)
    Access_secret = models.CharField(null=False, max_length=100, unique=True)
    Screen_Name = models.CharField(null=False, max_length=50, unique=True, validators=[validators.validate_slug])

    def __unicode__(self):
        return self.Screen_Name


class FavouriteKeywords(models.Model):
    Fav_key_id = models.IntegerField(primary_key=True)
    Fav_keywords = models.CharField(max_length=50, null=True, unique=True)
    num_limits = models.IntegerField( null=True, validators=[MinValueValidator(1)])
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __unicode__(self):
        return self.Fav_keywords


class RestrictedKeywords(models.Model):
    # validators = [validators.validate_slug]
    Res_key_id = models.IntegerField(primary_key=True)
    Restrited_keywords = models.CharField(max_length=100, null= True, unique= True,)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __unicode__(self):
        return self.Restrited_keywords


class Fav_Keywords(models.Model):
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE, related_name='account_id', null=True)
    keyword = models.ForeignKey(FavouriteKeywords, on_delete=models.CASCADE, null=True)
    num_limits = models.IntegerField(null=True,validators=[MinValueValidator(1)])


class Res_Keywords(models.Model):
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE)
    keyword = models.ForeignKey(RestrictedKeywords, on_delete=models.CASCADE)


class Black_List_Names(models.Model):
    Name_id = models.IntegerField(primary_key=True)
    block_users = models.CharField(max_length=100, null= True, unique=True ,validators=[validators.validate_slug])
    status = models.CharField(default='manual', max_length=10)

    def __unicode__(self):
        return self.block_users



class Black_user(models.Model):
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE)
    black_list = models.ForeignKey(Black_List_Names,  on_delete=models.CASCADE)



class days(models.Model):
    days_back = models.IntegerField(null=False, default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.days_back


class Jobs(models.Model):
    Job_id = models.IntegerField(primary_key=True, null=False)
    initial_time = models.DateTimeField(null=True, blank=True)
    final_time = models.DateTimeField(null=True, blank=True)
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = [ "initial_time", "final_time",]



class TweetsData(models.Model):
    id = models.IntegerField(primary_key=True)
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE, null=True, blank=True)
    tweet_id = models.IntegerField(null=True)
    tweet_content = models.CharField(max_length=1000, null=True)
    Name = models.CharField(max_length=1000, null=True)
    timestamp = models.DateField(auto_now=False, auto_now_add=True, null=True)
    status = models.BooleanField(default=True)
    jobs = models.ForeignKey(Jobs, default='', null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.tweet_id

    def __str__(self):
        return self.tweet_id


class LikeTweetsContent(models.Model):
    Account_id = models.ForeignKey(Accounts_Data, on_delete=models.CASCADE, null=True, blank=True)
    TweetContent = models.ForeignKey(TweetsData, on_delete=models.CASCADE, null=True, blank=True)
