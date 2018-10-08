from django.contrib import admin
from .models import *
# from .models import tweets_twitter ,tweets_numbering,using_time,Data_tweet

class user_credentials(admin.ModelAdmin):
    list_display = ["account", "Screen_Name", "Access_token", "Access_secret", "user"]

    class Meta:
        model = Accounts_Data


class Favourite_keywords(admin.ModelAdmin):
    list_display = [ "Fav_keywords",  "timestamp"]

    class Meta:
        model = FavouriteKeywords


class Restricted_word(admin.ModelAdmin):
    list_display = ["Res_key_id", "Restrited_keywords","timestamp"]

    class Meta:
        model = RestrictedKeywords


class Tweets_Data(admin.ModelAdmin):
    list_display = ["id", "tweet_id", "tweet_content", "timestamp"]

    class Meta:
        model = TweetsData





class Black_User(admin.ModelAdmin):
    list_display = [ "Name_id", "block_users", "status"]

    class Meta:
        model = Black_List_Names





class Fav_keyword_AssociateTable(admin.ModelAdmin):
    list_display = ["Account_id", "keyword"]

    class Meta:
        model = Fav_Keywords


class Res_keyword_AssociateTable(admin.ModelAdmin):
    list_display = ["Account_id", "keyword"]

    class Meta:
        model = Res_Keywords



class Black_List_AssociateTable(admin.ModelAdmin):
    list_display = ["Account_id", "black_list"]

    class Meta:
        model = Black_user



class LikeTweetsData(admin.ModelAdmin):
    list_display = ["Account_id", "TweetContent",]

    class Meta:
        model = LikeTweetsContent


admin.site.register(Accounts_Data,user_credentials)
admin.site.register(LikeTweetsContent,LikeTweetsData)
admin.site.register(FavouriteKeywords,Favourite_keywords)
admin.site.register(RestrictedKeywords,Restricted_word)
admin.site.register(TweetsData, Tweets_Data)
admin.site.register(Black_List_Names, Black_User)
admin.site.register(Fav_Keywords,Fav_keyword_AssociateTable)
admin.site.register(Res_Keywords,Res_keyword_AssociateTable)
admin.site.register(Black_user,Black_List_AssociateTable)
# admin.site.register(Jobs,User_Jobs)
