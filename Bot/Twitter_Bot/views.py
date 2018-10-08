import logging
import sys
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *
import tweepy
import datetime as dt
from datetime import timedelta
from .utils import *
from datetime import datetime
import time
from random import randint
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from time import sleep
import json
# Create your views here.
tweets_num = 0
number = 0
retweets = 0
twitter_handler_count = 0

def home(request):
    consumer_key='URCTNLThkHQAxCFLtMjWOnMlA'
    consumer_secret='lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y'
    auth = OAuthHandler(consumer_key, consumer_secret)
    # token = request.GET.get('oauth_token')
    verifier=request.GET.get('oauth_verifier')
    verifier=str(verifier)
    print ('Oauth_token',  '==> Oauth_verifier', verifier, 'Type of verifier ==>',type(verifier))
    token = request.session.get('request_token')
    # request.session['request_token'] = auth._get_request_token
    print(token)
    request.session.delete('request_token')
    print('after delete', token)
    auth.request_token = token
    # user = Accounts_Data.objects.get(user_id=id)
    try:
        acess_token = auth.get_access_token(verifier=verifier)
        print(acess_token)
        print(acess_token[0])
        print(acess_token[1])
        print('access token ',type(auth.access_token), auth.access_token)
        print('access token secret',type(auth.access_token_secret),auth.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        user = api.me()
        name = user.screen_name
        if Accounts_Data.objects.filter(Screen_Name=name).exists():
            messages.error(request,'This account is already registered')
            sys.exit(-1)
        auth.set_access_token(acess_token[0], acess_token[1])
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        id = request.user.id
        print(id)
        username = request.user.username
        print(username)
        new_data = Accounts_Data(Access_token=auth.access_token, Access_secret=auth.access_token_secret,
                        Screen_Name=user.screen_name, user_id=id)
        new_data.save()
        return api
    except BaseException as e:
        print (e)


def unlike_tweets_from_database(request, pk_id):
    form = Days_calc(request.POST or None)
    like_tweets = 0
    unlike_tweets = 0
    days_back = None
    id = int(pk_id)
    consumer_key = 'URCTNLThkHQAxCFLtMjWOnMlA'
    consumer_secret = 'lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y'
    user_data_id = None
    print(id)
    id_field = Accounts_Data.objects.get(account=id)
    print('Id of Account',id_field)
    if request.user.is_active:
        user_data_id = request.user.id
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    object = LikeTweetsContent.objects.filter(Account_id=id)
    data = [data_tweet.id for data_tweet in object]
    if len(data) == 0:
        messages.error(request,'You have liked nothing,No data to unlike')
        return redirect('/home_page/Account_id/%d/#fav_keywords/'%id)
    if id is None:
        messages.error(request, 'Please select any account')
    print("Id of tokens", id)
    # del request.session["id"]
    get_data = Accounts_Data.objects.get(account=id)
    access_token = get_data.Access_token
    access_secret = get_data.Access_secret
    check_point_keys = [key.user_id for key in tokens]
    if len(check_point_keys) == 0:
        messages.error(request, 'please Enter your credentials to go further')
        return redirect('/home_page/Account_id/%d/' % id)
    else:
        pass
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    user = api.me()
    date_time = None
    if request.method == 'POST' :
        if form.is_valid():
            for data in object:
                try:
                    days_back = form.data['days_back']
                    days_back = int(days_back)
                    Id_of_tweet = data.TweetContent.tweet_id
                    timestamp = data.TweetContent.timestamp
                    tweet_of_Id = api.get_status(id=Id_of_tweet)
                    now = dt.datetime.now().date()
                    previous = dt.timedelta(days=days_back)
                    date_time = now - previous
                    # if timestamp >= date_time and timestamp <= now:
                    if timestamp == date_time:
                        if tweet_of_Id.favorited:
                            unlike = api.destroy_favorite(tweet_of_Id.id)
                            like_tweets +=1
                            print('------->>>',unlike)
                            Like_tweet_DB = TweetsData.objects.filter(tweet_id=Id_of_tweet).update(status=False)
                        elif not tweet_of_Id.favorited:
                            print ('This tweet is being unliked')
                            Like_tweet_DB = TweetsData.objects.filter(tweet_id= Id_of_tweet).update(status=False)
                    else:
                        unlike_tweets +=1
                except BaseException as e:
                    print (str(e), )
        elif not form.is_valid():
            messages.error(request,'Please enter valid data')
    if like_tweets>=1:
        messages.error(request,'%d Tweets unliked before days you given'%like_tweets)
        return redirect('/home_page/Account_id/%d/' % id)
    if unlike_tweets>=1:
        messages.error(request, '%d days back! %d tweets are already unlike'%(days_back,unlike_tweets))
        return redirect('/home_page/Account_id/%d/' % id)
    return render(request , 'home_tweets.html', {'form':form,'object':object,'id':id,'tokens':tokens})


def check_followers(request):
    names_count = 0
    names_added = 0
    logging.info("begin")
    consumer_key = 'URCTNLThkHQAxCFLtMjWOnMlA'
    consumer_secret = 'lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y'
    user_data_id = None
    id = request.session["id"]
    print(id)
    # if request.is_ajax:
    names_not_added = []
    id_field = Accounts_Data.objects.get(account=id)
    print(id_field)
    if request.user.is_active:
        user_data_id = request.user.id
        print(user_data_id)
        user_data_name = request.user.username
        print(user_data_name)
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    if id is None:
        messages.error(request,'Please select any account')
    print("Id of tokens",id)
    # del request.session["id"]
    data = Accounts_Data.objects.get(account=id)
    access_token = data.Access_token
    access_secret = data.Access_secret
    check_point_keys = [ key.user_id for key in tokens]
    if len(check_point_keys)== 0 :
        messages.error(request, 'please Enter your credentials to go further')
        return redirect('/home_page/Account_id/%d/'%id)
    else:
        pass
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    user = api.me()
    screen_name = user.screen_name
    follow = api.followers(screen_name=str(screen_name))
    user_obj = LikeTweetsContent.objects.filter(Account_id=id)
    # get screen names of user from DB as a list
    names = [name.TweetContent.Name for name in user_obj]
    print (names)
    unique = set(names)
    # unique = list(unique)
    print ('List of uniques names from DB', unique)
    print (type(unique))
    if len(unique) == 0:
        messages.error(request,'You have liked No one tweets')
        return redirect('/home_page/Account_id/%d/' % id)
    # get screen name of followers of my account as a list
    following = [followers.screen_name for followers in follow]
    print(following)
    print (type(following))
    follow = set(following)
    data_of_tweets = TweetsData.objects.filter(Account_id=id)
    data_of_Name = [names.Name for names in data_of_tweets]
    print(data_of_Name)
    # follow = list(unique)
    for name in unique:
        name = str(name)
        print (name)
        if name in follow:
            messages.error(request,'%d has followed us'%name)
            print('He has followed us ---',name)
        if name not in follow:
            try:
                status_object = api.get_user(screen_name=name)
                followers_count = status_object._json[u'followers_count']
                print (followers_count)
                print (status_object)
                if followers_count < 1000:
                    # block = api.create_block(screen_name=name)
                    block = 'blocked'
                    print ('===>',block, 'blocked ==>>',name)
                    if Black_List_Names.objects.filter(block_users=name).exists():
                        Black_names = Black_List_Names.objects.only('Name_id').get(
                            block_users=name).Name_id
                        print(Black_names)
                        Black_names_id = Black_List_Names.objects.get(Name_id=Black_names)
                        print(Black_names_id)
                        data_save = Black_user(Account_id=id_field, black_list=Black_names_id)
                        data_save.save()
                    blocked_name = Black_List_Names(block_users=name, status='automatic', )
                    blocked_name.save()
                    Black_user_name = Black_List_Names.objects.only('Name_id').get(block_users=name).Name_id
                    print(Black_user_name)
                    Get_Black_name = Black_List_Names.objects.get(Name_id=Black_user_name)
                    print(Get_Black_name)
                    black_user = Black_user(Account_id=id_field, black_list=Get_Black_name)
                    black_user.save()
                    names_added += 1
                elif followers_count >= 1000:
                    print('This user is not blocked .... ', name)
                    names_not_added.append(name)
                    print( type(names_not_added),names_not_added)
                    counter_for_name = data_of_Name.count(name)
                    if counter_for_name>=3:
                        blocked_name = Black_List_Names(block_users=name, status='automatic')
                        blocked_name.save()
                        Black_user_name = Black_List_Names.objects.only('Name_id').get(block_users=name).Name_id
                        print(Black_user_name)
                        Get_Black_name = Black_List_Names.objects.get(Name_id=Black_user_name)
                        print(Get_Black_name)
                        black_user = Black_user(Account_id=id_field, black_list=Get_Black_name)
                        black_user.save()
                        names_count +=1
            except BaseException as e:
                print (str(e))
    if names_added >1:
        messages.error(request,'%d names added in Black list!Tweet like less then 1000'%names_added)
        return redirect('/home_page/Account_id/%d/' % id)

    if names_count >1:
        messages.error(request,'%d names added in Black list! You Like their tweets But user did not follow you'%names_count)
        return redirect('/home_page/Account_id/%d/' % id)

    # if names_added or names_count ==0:
    #     messages.info(request,'No names added in Black list')
    #     return redirect('/home_page/Account_id/%d/' % id)

        # if len(names_not_added) != 0:
        #     messages.error(request, '%s not added in blacklist bcz i did not like their more then 3 tweets' % names_not_added)
        #     redirect('/home_page/Account_id/%d/' % id)
    return redirect('/home_page/Account_id/%d/'%id)


def data_del(request):
    data = FavouriteKeywords.objects.all()
    ids_list = []
    for data_del in data:
        ids = data_del.id
        ids_list.append(ids)
    for model in ids_list:
        get_object_or_404(FavouriteKeywords, id=model).delete()
    return redirect('/home_page/main_page/#fav_keywords')


def edit_detail(request, pk_id):
    form_1 = Fav_keyword(request.POST or None)
    pk = int(pk_id)
    object = FavouriteKeywords.objects.all()
    instance =get_object_or_404(FavouriteKeywords, pk=pk)
    form = Fav_keyword(request.POST or None, instance=instance)
    print ('---' ,instance)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('/home_page/main_page/#fav_keywords')
    else:
        form = Fav_keyword(instance=instance)
    return render(request,'test.html',{'form':form, 'form_1':form_1})


def delete_product(request, pk_id =None):
    try:
        id = request.session["id"]
        pk_id = int(pk_id)
        # object = Fav_Keywords.objects.get(id= pk_id)
        object = get_object_or_404(Fav_Keywords, id=pk_id)
        object.delete()
        return redirect('/home_page/Account_id/%d/#fav_keywords' % id)
    except BaseException as e:
        print(e)

    return redirect('/home_page/Account_id/%d/#fav_keywords' % id)


def Del_all_data_of_block_user(request):
    data = Black_List_Names.objects.all()
    for data_id in data:
        get_object_or_404(Black_List_Names, id=data_id.id).delete()
    return redirect('/home_page/main_page/#res')


def delete_block_user(request,pk_id =None):
    try:
        id = request.session["id"]
        print(id)
        pk_id = int(pk_id)
        object = get_object_or_404(Black_user,id=pk_id)
        object.delete()
        return redirect('/home_page/Account_id/%d/#res'%id)
    except BaseException as e:
        print(e)
    return redirect('/home_page/Account_id/%d/#res' % id)


def Restricted_word(request, pk_id=None):
    try:
        id = request.session["id"]
        pk_id = int(pk_id)
        get_object_or_404(Res_Keywords,id= pk_id).delete()
        return redirect('/home_page/Account_id/%d/#res_keywords'%id)
    except BaseException as e:
        print(e)
    return redirect('/home_page/Account_id/%d/#fav_keywords' % id)


def Delete_all_restricted_words(request):
    data = RestrictedKeywords.objects.all()
    ids_list = []
    for data_del in data:
        ids = data_del.id
        ids_list.append(ids)
    for model in ids_list:
        get_object_or_404(RestrictedKeywords, id=model).delete()
    return redirect('/home_page/#res_keywords')


def edit_restricted_keywords(request, pk_id):
    pk = int(pk_id)
    object = RestrictedKeywords.objects.all()
    instance = get_object_or_404(RestrictedKeywords, pk=pk)
    form = Restricted_word(request.POST or None, instance=instance)
    print ('---', instance)
    if request.method == 'POST':
        # form = Fav_keyword(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        return redirect('/home_page/#res_keywords')
    else:
        form = Restricted_word(instance=instance)
        # restricted_word_tweets is an old template replace by test_html
    return render(request, 'test.html', {'form': form, 'object':object, })


@login_required(login_url='/home_page/')
def account_info(request, pk_id=None):
    user_data_id = None
    username = None
    id = int(pk_id)
    flag = False
    #set Account id in sessions which is being use in [performance as a whole]
    request.session["id"] = id
    instance = get_object_or_404(Accounts_Data, account=id)
    print(instance)
    print(id)
    id_field = Accounts_Data.objects.get(account=id)
    if request.user.is_authenticated:
        username = request.user.username
        username = str(username)
    if request.user.is_active:
        user_data_id = request.user.id
        print(user_data_id)
        user_data_name = request.user.username
        print(user_data_name)
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    # object = FavouriteKeywords.objects.all()
    object = Fav_Keywords.objects.filter(Account_id=id)
    form = Fav_keyword(request.POST or None)
    form_1 = Restricted_word(request.POST or None)
    # object_like = RestrictedKeywords.objects.all()
    object_like = Res_Keywords.objects.filter(Account_id=id)
    # object_block_user = Black_List_Names.objects.all()
    object_block_user = Black_user.objects.filter(Account_id=id)
    form_2 = BlockUser(request.POST or None)
    form_3 = between_time(request.POST or None)
    sleep(0.7)
    try:
        if Accounts_Data.objects.only('account').get(Screen_Name=instance).account:
            print("True")
            if request.method == 'POST':
                try:
                    if form.is_valid():
                        string = (form.data['Fav_keywords'])
                        string = str(string)
                        string = string.lower().strip()
                        num = (form.data['num_limits'])
                        num = int(num)
                        checker = Res_Keywords.objects.filter(Account_id=id_field)
                        checker_data = [data.keyword.Restrited_keywords for data in checker]
                        print(checker_data)
                        if string in checker_data:
                            print(string)
                            messages.error(request,'Keyword must not same from Restricted Keywords')
                            return redirect('/home_page/Account_id/%d/#checker' % id)
                        if FavouriteKeywords.objects.filter(Fav_keywords=string).exists():
                            Favourite_keyword_id = FavouriteKeywords.objects.only('Fav_key_id').get(Fav_keywords=string).Fav_key_id
                            print(Favourite_keyword_id)
                            if not Fav_Keywords.objects.filter(Account_id=id_field,keyword_id=Favourite_keyword_id).exists():
                                Favourite_kw_id = FavouriteKeywords.objects.get(Fav_key_id=Favourite_keyword_id)
                                print(Favourite_kw_id)
                                data_save = Fav_Keywords(Account_id=id_field, keyword=Favourite_kw_id, num_limits=num)
                                data_save.save()
                                return redirect('/home_page/Account_id/%d/#checker' % id)
                            if Fav_Keywords.objects.filter(Account_id=id_field,keyword_id=Favourite_keyword_id).exists():
                                messages.error(request, 'Keyword already exist')
                                return redirect('/home_page/Account_id/%d/#checker' % id)

                        if not FavouriteKeywords.objects.filter(Fav_keywords=string).exists():
                            data_save = FavouriteKeywords(Fav_keywords=string,num_limits=num)
                            data_save.save()
                            Favourite_keyword_id = FavouriteKeywords.objects.only('Fav_key_id').get(
                                Fav_keywords=string).Fav_key_id
                            print(Favourite_keyword_id)
                            Favourite_kw_id = FavouriteKeywords.objects.get(Fav_key_id=Favourite_keyword_id)
                            print(Favourite_kw_id)
                            data_save = Fav_Keywords(Account_id=id_field, keyword=Favourite_kw_id, num_limits=num)
                            data_save.save()
                            return redirect('/home_page/Account_id/%d/#fav_keywords' % id)

                    elif not form.is_valid():
                        string = (form.data['Fav_keywords'])
                        string = str(string)
                        string = string.strip()
                        num = (form.data['num_limits'])

                        if not num.isdigit():
                            messages.error(request,'please enter integer value i-e 3')
                            return redirect('/home_page/Account_id/%d/#checker' % id)
                        num = int(num)
                        checker = Res_Keywords.objects.filter(Account_id=id_field)
                        checker_data = [data.keyword.Restrited_keywords for data in checker]
                        print(checker_data)
                        if string in checker_data:
                            print(string)
                            messages.error(request, 'Keyword must not be same from Restricted Keywords')
                            return redirect('/home_page/Account_id/%d/#checker' % id)

                        Favourite_keyword_id = FavouriteKeywords.objects.only('Fav_key_id').get(
                            Fav_keywords=string).Fav_key_id
                        print(Favourite_keyword_id)
                        Favourite_kw_id = FavouriteKeywords.objects.get(Fav_key_id=Favourite_keyword_id)
                        print(Favourite_kw_id)

                        if Fav_Keywords.objects.filter(Account_id=id_field, keyword_id=Favourite_keyword_id).exists():
                            messages.error(request, 'Keyword already exist')
                            return redirect('/home_page/Account_id/%d/#checker' % id)

                        if FavouriteKeywords.objects.filter(Fav_keywords=string, num_limits=num).exists():
                            print('Done')
                            # Favourite_keyword_id = FavouriteKeywords.objects.only('Fav_key_id').get(Fav_keywords=string).Fav_key_id
                            # print(Favourite_keyword_id)
                            # Favourite_kw_id = FavouriteKeywords.objects.get(Fav_key_id=Favourite_keyword_id)
                            # print(Favourite_kw_id)
                            data_save = Fav_Keywords(Account_id=id_field, keyword=Favourite_kw_id, num_limits=num)
                            data_save.save()
                            return redirect('/home_page/Account_id/%d/#fav_keywords'%id)
                        elif not FavouriteKeywords.objects.filter(Fav_keywords=string, num_limits=num).exists():
                            print('ok')
                            Favourite_keyword_id = FavouriteKeywords.objects.only('Fav_key_id').get(
                                Fav_keywords=string).Fav_key_id
                            print(Favourite_keyword_id)
                            Favourite_kw_id = FavouriteKeywords.objects.get(Fav_key_id=Favourite_keyword_id)
                            print('fav keyword',Favourite_kw_id)
                            data_save = Fav_Keywords(Account_id=id_field, keyword=Favourite_kw_id, num_limits=num)
                            data_save.save()
                            return redirect('/home_page/Account_id/%d/#fav_keywords'%id)
                        messages.error(request,'Enter valid data')
                        return redirect('/home_page/Account_id/%d/#checker' % id)
                except BaseException as e:
                    print(e)
                    try:
                        if form_1.is_valid():
                            string = (form.data['Restrited_keywords'])
                            string = str(string)
                            string = string.lower().strip()
                            print(string)
                            checker = Fav_Keywords.objects.filter(Account_id=id_field)
                            checker_data = [data.keyword.Fav_keywords for data in checker]
                            print(checker_data)
                            if string in checker_data:
                                print(string)
                                messages.error(request, 'Keyword must not same from Favorite Keyword')
                                return redirect('/home_page/Account_id/%d/#checker' % id)
                            if RestrictedKeywords.objects.filter(Restrited_keywords=string).exists():
                                Restricted_keyword_id = RestrictedKeywords.objects.only('Res_key_id').get(Restrited_keywords=string).Res_key_id
                                print(Restricted_keyword_id)
                                Restricted_kw_id = RestrictedKeywords.objects.get(Res_key_id=Restricted_keyword_id)
                                print(Restricted_kw_id)
                                if Res_Keywords.objects.filter(Account_id=id_field,
                                                               keyword_id=Restricted_keyword_id).exists():
                                    messages.error(request, 'keyword  already exist')
                                    return redirect('/home_page/Account_id/%d/#checker' % id)
                                if not Res_Keywords.objects.filter(Account_id=id_field,
                                                               keyword_id=Restricted_keyword_id).exists():
                                    data_save = Res_Keywords(Account_id=id_field , keyword=Restricted_kw_id)
                                    data_save.save()
                                    return redirect('/home_page/Account_id/%d/#res_keywords'%id)
                            if not RestrictedKeywords.objects.filter(Restrited_keywords=string).exists():
                                data_save = RestrictedKeywords(Restrited_keywords=string)
                                data_save.save()
                                Restricted_keyword_id = RestrictedKeywords.objects.only('Res_key_id').get(
                                    Restrited_keywords=string).Res_key_id
                                print(Restricted_keyword_id)
                                Restricted_kw_id = RestrictedKeywords.objects.get(Res_key_id=Restricted_keyword_id)
                                print(Restricted_kw_id)
                                data_save = Res_Keywords(Account_id=id_field, keyword=Restricted_kw_id)
                                data_save.save()
                                return redirect('/home_page/Account_id/%d/#res_keywords' % id)
                        elif not form_1.is_valid():
                            string = (form.data['Restrited_keywords'])
                            string = str(string)
                            string = string.lower().strip()
                            checker = Fav_Keywords.objects.filter(Account_id=id_field)
                            checker_data = [data.keyword.Fav_keywords for data in checker]
                            print(type(checker_data))
                            if string in checker_data:
                                print(string)
                                messages.error(request, 'Keyword must not be same from Favorite Keyword')
                                return redirect('/home_page/Account_id/%d/#checker' % id)
                            Restricted_keyword_id = RestrictedKeywords.objects.only('Res_key_id').get(Restrited_keywords=string).Res_key_id
                            print(Restricted_keyword_id)
                            Restricted_kw_id = RestrictedKeywords.objects.get(Res_key_id=Restricted_keyword_id)
                            print(Restricted_kw_id)
                            if Res_Keywords.objects.filter(Account_id=id_field,keyword_id=Restricted_keyword_id).exists():
                                messages.error(request,'keyword  already exist')
                                return redirect('/home_page/Account_id/%d/#checker' % id)
                            if RestrictedKeywords.objects.filter(Restrited_keywords=string).exists():
                                data_save = Res_Keywords(Account_id=id_field, keyword=Restricted_kw_id)
                                data_save.save()
                                return redirect('/home_page/Account_id/%d/#res_keywords' % id)
                    except BaseException as e:
                        print(e)
                    try:
                        if form_2.is_valid():
                            instance = form_2.save()
                            string = (form.data['block_users'])
                            string = str(string)
                            string = string.strip()
                            print (string)
                            black_list_id = Black_List_Names.objects.only('Name_id').get(block_users=string).Name_id
                            print(black_list_id)
                            black_list_name = Black_List_Names.objects.get(block_users=string)
                            print(black_list_name)
                            data_save = Black_user(Account_id= id_field, black_list=black_list_name)
                            data_save.save()
                            return redirect('/home_page/Account_id/%d/#checker'%id)
                        elif not form_2.is_valid():
                            string = (form.data['block_users'])
                            string = str(string)
                            string = string.strip()
                            black_list_name = Black_List_Names.objects.get(block_users=string)
                            print(black_list_name)
                            if Black_user.objects.filter(Account_id=id_field, black_list=black_list_name).exists():
                                messages.error(request, 'User name already exist')
                                return redirect('/home_page/Account_id/%d/#checker' % id)
                            if Black_List_Names.objects.filter(block_users=string).exists():
                                black_list_id = Black_List_Names.objects.only('Name_id').get(block_users=string).Name_id
                                print(black_list_id)
                                data_save = Black_user(Account_id=id_field, black_list=black_list_name)
                                data_save.save()
                                return redirect('/home_page/Account_id/%d/#res' % id)
                    except BaseException as e:
                        print(e)
            elif request.method == 'GET':
                # form_3 = between_time(request.POST or None)
                if request.GET.get('initial_time') and request.GET.get('final_time') == None:
                    return redirect('/home_page/Account_id/%d/' % id)

                elif request.GET.get('initial_time') and request.GET.get('final_time') != None:
                    initial_datetime = request.GET.get('initial_time')
                    final_datetime = request.GET.get('final_time')
                    print(type(initial_datetime))
                    print(type(initial_datetime), initial_datetime)
                    print(type(final_datetime))
                    print(type(final_datetime), final_datetime)
                    object = Fav_Keywords.objects.filter(Account_id=id)
                    check_point = [data.keyword.Fav_keywords for data in object]
                    if len(check_point) == 0:
                        messages.error(request, 'please enter favourite keywords')
                        return redirect('/home_page/Account_id/%d/#checker' % id)

                    if final_datetime <= initial_datetime:
                        messages.error(request, 'Please enter correct date and time')
                        print ('Please enter correct date')
                        return redirect('/home_page/main_page/#checker/')
                    elif final_datetime > initial_datetime:
                        initial_date = timezone.datetime.strptime("{}".format(initial_datetime), '%m/%d/%Y %I:%M %p')
                        print('type of initial_date', type(initial_date))
                        initial_date = initial_date.replace(tzinfo=None)
                        print(initial_date)
                        final_date = timezone.datetime.strptime("{}".format(final_datetime), '%m/%d/%Y %I:%M %p')
                        print('type of final_date', type(final_date))
                        print(final_date)
                        current_time = datetime.now() + timedelta(hours=5)
                        print(current_time)
                        current_time = current_time.strftime("%m/%d/%Y %H:%M")
                        print(current_time)
                        current_time = timezone.datetime.strptime("{}".format(current_time), '%m/%d/%Y %H:%M')
                        print(current_time)
                        if current_time > initial_date:
                            print('less time')
                            messages.error(request,'Initial time should be greater or equal to system time')
                            return redirect('/home_page/Account_id/%d/#checker/' % id)
                        PERIOD = (final_date - initial_date).total_seconds()
                        print(PERIOD)
                        if PERIOD < 0:
                            messages.error(request,'Please Enter correct date and time!')
                            return redirect('/home_page/Account_id/%d/#checker/' % id)
                        save_into_DB = Jobs(initial_time=initial_date, final_time=final_date, Account_id=id_field)
                        save_into_DB.save()
                        flag = True
                        # return redirect('/home_page/main_page/Account_id/%d/#time'%id)
            else:
                form = Fav_keyword(request.POST or None)
                form_1 = Restricted_word(request.POST or None)
                form_2 = BlockUser(request.POST or None)
                form_3 = between_time(request.POST or None)
    except BaseException as e:
        print(e)
    return render(request, 'test.html',
                      {'tokens': tokens, 'form': form, 'object': object, 'form_1': form_1, 'object_like': object_like,
                       'form_2': form_2, 'object_block_user': object_block_user, 'form_3': form_3,
                       'flag':flag,
                      }
                  )


@login_required(login_url='/home_page/signin/')
def performance_as_whole(request,pk_id=None):
    global tweets_num
    global number
    global twitter_handler_count
    global retweets
    id = int(pk_id)
    user_data_id = None
    consumer_key = 'URCTNLThkHQAxCFLtMjWOnMlA'
    consumer_secret = 'lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y'
    access_token = ''
    access_secret = ''
    Screen_Name = ''
    #id for Twitter Accounts user
    instance = get_object_or_404(Accounts_Data, account=id)
    print(instance)
    print(id)
    id_field = Accounts_Data.objects.get(account=id)
    print(id_field)
    if request.user.is_active:
        user_data_id = request.user.id
        print(user_data_id)
        user_data_name = request.user.username
        print(user_data_name)
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    if id is None:
        messages.error(request,'Please select any account')
    print('IN THIS VIEW CHECKER****')
    print("Id of tokens",id)
    data = Accounts_Data.objects.get(account=id)
    access_token = data.Access_token
    access_secret = data.Access_secret
    check_point_keys = [ key.user_id for key in tokens]
    if len(check_point_keys)== 0 :
        messages.error(request, 'please Enter your credentials to go further')
        return redirect('/home_page/Account_id/%d/'%id)
    else:
        pass
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    user = api.me()
    print(user.screen_name)
    logging.info("begin")
    sleep(2.5)
    like_data = []
    object = FavouriteKeywords.objects.all()
    restricted_object = Res_Keywords.objects.filter(Account_id=id)
    data_to_watch = TweetsData.objects.all()
    # object = FavouriteKeywords.objects.all()
    object = Fav_Keywords.objects.filter(Account_id=id)
    check_point = [data.keyword.Fav_keywords for data in object]
    if len(check_point) == 0:
        messages.error(request,'please enter Favourite keywords')
        return redirect('/home_page/Account_id/%d/perform' % id)
    # black_list = Black_List_Names.objects.all()
    black_list_data = Black_user.objects.filter(Account_id=id)
    black_list_words = [words.black_list.block_users for words in black_list_data]
    print(black_list_words)
    follow = api.followers(screen_name=Screen_Name)
    following = [followers.screen_name for followers in follow]
    print(following)
    print (type(following))
    #getting time for liking tweets from database
    getting_time = Jobs.objects.filter(Account_id=id).latest('Job_id')
    print(getting_time)
    jobs_id = getting_time.Job_id
    print(jobs_id)
    initial_time = getting_time.initial_time
    final_time = getting_time.final_time
    time = str(initial_time)
    print('type of initial time',type(initial_time))
    time_2 = str(final_time)
    print('type of final time',type(final_time))
    PERIOD = (final_time - initial_time).total_seconds()
    print(PERIOD)
    if PERIOD<0:
        messages.error(request,'Please enter correct datetime')
        return redirect('/home_page/Account_id/%d/#fav_keywords/'%id)
    elif not PERIOD < 0:
        pass
    if request.is_ajax:
        block_users = Black_List_Names.objects.all()
        datetime_list = []
        for n in range(3):
            dt = initial_time + timedelta(seconds=randint(0, PERIOD))
            dt = dt.replace(tzinfo=None)
            print(dt)
            datetime_list.append(dt)
        datetime_list.sort()
        print(datetime_list)
        for date_time in datetime_list:
            date_time = (date_time)
            print(date_time)
            date_time = str(date_time)
            print(type(date_time))
            flag = True
            while flag:
                current_time_2 = datetime.now() + timedelta(hours=5)
                current_time_2 = current_time_2.strftime("%Y-%m-%d %H:%M:%S")
                current_time_2 = str(current_time_2)
                print ('current time', current_time_2)
                if str(current_time_2).__contains__(date_time):
                    for usi in object:
                        print (usi.keyword.Fav_keywords)
                        fav_keyword = usi.keyword.Fav_keywords
                        print (fav_keyword)
                        num = usi.num_limits
                        print(num)
                        list_words = [words.keyword.Restrited_keywords for words in restricted_object]
                        list_words = list_words
                        print(list_words)
                        tweets = tweepy.Cursor(api.search, q=fav_keyword, rpp=100, result_type='mixed', tweet_mode="extended").items(num)
                        for tweet in tweets:
                            try:
                                twitter_handler = tweet.user.screen_name
                                if twitter_handler in black_list_words:
                                    if not twitter_handler in follow:
                                        twitter_handler_count +=1
                                        continue
                                    if twitter_handler in follow:
                                        pass
                                        if ('RT @' in tweet.text):
                                            continue
                                if any(restrict_word in tweet.full_text for restrict_word in list_words):
                                    if not tweet.favorited:
                                        number +=1
                                        print('restricted words found ', tweet.full_text)
                                    if tweet.favorited:
                                        unlike = api.destroy_favorite(tweet.id)
                                        print ('==>>', unlike.text)
                                        continue
                                if not any(restrict_word in tweet.full_text for restrict_word in list_words):
                                    # if tweet.favorite_count >= 3:
                                    if ('RT @' in tweet.full_text):
                                        retweets +=1
                                        continue
                                    if not tweet.favorited:
                                        print(type(tweet.full_text))
                                        name = tweet.user.screen_name
                                        print(name)
                                        like = api.create_favorite(tweet.id)
                                        print (like)
                                        tweets_num +=1
                                        like_data.append(like)
                                        new_tweets = TweetsData(tweet_id=tweet.id, tweet_content=like.text,
                                                                      Name=name,
                                                                      timestamp=tweet.created_at, jobs= getting_time,Account_id=id_field)
                                        new_tweets.save()
                                        Tweet_content = TweetsData.objects.only('id').get(tweet_content=like.text).id
                                        print(Tweet_content)
                                        Tweet_like_content = TweetsData.objects.get(id=Tweet_content)
                                        like_tweets = LikeTweetsContent(Account_id=id_field, TweetContent = Tweet_like_content)
                                        like_tweets.save()
                                        flag = False
                                        if ('RT @' in tweet.full_text):
                                            continue
                                    if tweet.favorited:
                                        print('Tweet is already liked')
                                    # elif tweet.favorite_count < 3:
                                    #     print(tweet.id, 'You have less then 3 likes')
                                    #
                                    #     if ('RT @' in tweet.text):
                                    #         continue
                            except BaseException as e:
                                name = tweet.user.screen_name
                                print (str(e), tweet.id,)
                elif str(current_time_2) > (date_time):
                    break
                else:
                    print('current time===>', current_time_2, 'date time ====>', date_time)
        try:
            # if number >=1:
            #     data = number
            #     data = {
            #         'is_taken': data
            #     }
            #     if data['is_taken']:
            #         data['error_message'] = 'Restricted words found in %d Tweets'%number
            #         return JsonResponse(data)
            if number>=1:
                messages.error(request,'restricted words in %d tweets'%number)
                return redirect('/home_page/Like_Tweets/')
            if tweets_num or retweets >= 1:
                messages.info(request, '%dTweets Liked!%dRetweeted Tweets are not liked'%(tweets_num,retweets))
                return redirect('/home_page/Like_Tweets/')
        except BaseException as e:
            print(e)
    else:
        print('Not an Ajax')
    return render(request, 'test.html', {'tokens':tokens,'id':id})


@login_required(login_url='/home_page/signin/')
def main_page(request):
    api = home(request)
    current_tokens_id = None
    user_data_id = None
    if request.user.is_authenticated:
        username = request.user.username
        username = str(username)
        print('NAME OF USER**',username)
    if request.user.is_active:
        user_data_id = request.user.id
        print('USER ID**',user_data_id)
        user_data_name = request.user.username
        print('USER NAME**',user_data_name)
    if Accounts_Data.objects.filter(user_id=user_data_id).exists():
        tokens = Accounts_Data.objects.filter(user_id=user_data_id)
        for Handler in tokens:
            if Handler.Screen_Name:
                id = Handler.account
                return redirect('/home_page/Account_id/%d/'%id)
            if not Handler.Screen_Name:
                messages.error(request,'You have not login your account, please Login Twitter Account First')
    return render(request,'home.html')


def del_keys(request):
    user_data_id = None
    if request.user.is_active:
        user_data_id = request.user.id
        print(user_data_id)
        user_data_name = request.user.username
        print(user_data_name)
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    pk_id = request.session["id"]
    pk_id = int(pk_id)
    print('ID OF Account**',pk_id)
    object = get_object_or_404(Accounts_Data, account = pk_id)
    print(object)
    deleted = object.delete()
    for handler in tokens:
        id = handler.account
        if id:
            return redirect('/home_page/Account_id/%d/'%id)
        elif not id:
            messages.error(request,'Please login with your Twitter Account')
            return redirect('/home_page/Account_Delete/')
    messages.info(request, 'Account deleted')
    return render(request,'home.html',{'pk_id':pk_id} )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home_page/signin/')
    else:
        form = SignUpForm()
    return render(request, 'signupform.html', {'form': form})


def SignIn(request):
    title = "Login Your Account"
    form = SimpleForm(request.POST or None)
    if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user= authenticate(username=username, password=password)
                if not user:
                    messages.error(request,"Name or password is incorrect")
                    return redirect('/home_page/signin/')
                if user is not None and user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    print(request.user.is_authenticated)
                    return redirect('/home_page/main_page/')
                else:
                    messages.error(request,'Invalid username/password!')
    context = {
            'form':form,
            'title':title,
        }
    return render(request,'signin.html', context)


def Signout(request):
     logout(request)
     return redirect('/home_page/signin/')


def like_tweets_data(request):
    id = request.session["id"]
    user_data_id = None
    if request.user.is_active:
        user_data_id = request.user.id
        print(user_data_id)
        user_data_name = request.user.username
        print(user_data_name)
    tokens = Accounts_Data.objects.filter(user_id=user_data_id)
    like_data =LikeTweetsContent.objects.filter(Account_id=id)
    return render(request,'All_Like_Tweets.html',{'like_data':like_data, 'tokens':tokens})


def tweets_data_del(request,pk_id):
    pk = int(pk_id)
    print(pk)
    instance = LikeTweetsContent.objects.filter(id=pk)
    print(instance)
    instance.delete()
    return redirect('/home_page/Like_Tweets/')


def keywords_checker(request):
    id = request.session['id']
    id = int(id)
    object = Fav_Keywords.objects.filter(Account_id=id)
    check_point = [data.keyword.Fav_keywords for data in object]
    if len(check_point) == 0:
        data = 'Hello'
        data = {
            'is_taken': data
        }
        if data['is_taken']:
            data['error_message'] = 'Empty form! Please enter Favouite keyword'
            return JsonResponse(data)
    return render(request,'test.html')


def check_like_tweets_number(request):
    global tweets_num
    if tweets_num >=1:
        messages.error(request, '%d Tweets liked previously' %(tweets_num))

    return render(request,'test.html')

