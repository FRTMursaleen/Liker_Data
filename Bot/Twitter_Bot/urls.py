from django.conf.urls import url,include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'Twitter_Bot'
urlpatterns = [
    # url('boxes/', views.name_of_the_page, name='name'),
    url('unlike_tweet/(?P<pk_id>[0-9]+)/', views.unlike_tweets_from_database, name='Unlike'),
    url('follow/', views.check_followers, name='Follows'),
    url('delete/', views.data_del, name="Clear_Data"),
    url('edit/(?P<pk_id>[0-9]+)/', views.edit_detail, name='update_data'),
    url('Delete_selective/(?P<pk_id>[0-9]+)/', views.delete_product, name='delete_fav_data'),
    url('Clear_All_block_users/', views.Del_all_data_of_block_user, name='Clear_restrictesd_words'),
    url('Delete_Block_user/(?P<pk_id>[0-9]+)/', views.delete_block_user, name='delete_data'),
    url('Delete_restricted_words/(?P<pk_id>[0-9]+)/', views.Restricted_word, name='delete_restricted_data'),
    url('Delete_all_restricted_words/', views.Delete_all_restricted_words, name='delete_all_restricted_words'),
    url('edit_restricted_words/(?P<pk_id>[0-9]+)/', views.edit_restricted_keywords, name='update_restricted_data'),
    url('verifier/',views.verification,name='verifier'),
    url('Account_id/(?P<pk_id>[0-9]+)/',views.account_info,name='help'),
    url('register/', views.home, name='register'),
    # url('signup/', views.signup, name='signup'),
    url('Account_Delete/', views.del_keys,name='delete_keys'),
    url('keywords_checker',views.keywords_checker,name='keywords_checker'),
    url('like_checker',views.check_like_tweets_number,name='checker_count'),
    url('(?P<pk_id>[0-9]+)/performance/', views.performance_as_whole, name='perform'),
    url('Like_Tweets/', views.like_tweets_data, name='Like_Tweets'),
    url('signout/', views.Signout, name='signout'),
    url('cheking/(?P<pk_id>[0-9]+)/', views.tweets_data_del, name='cheking'),
    # url('main_page/', views.all_together, name='home'),
    url('main_page/', views.main_page, name='home'),
    url('signin/', views.SignIn, name='signin'),
    url('', views.signup, name='signup'),

]

