import tweepy
from tweepy import OAuthHandler
import webbrowser
from tweepy.auth import OAuthHandler
import requests
from requests_oauthlib import OAuth1

from django.shortcuts import render, render_to_response, redirect, get_object_or_404,HttpResponse,HttpResponseRedirect

# def setTwitterAuth():
#     consumer_key = 'btajWcCdHsqGckzWKg8cT42Ss'
#     consumer_secret = '3A9bzg07e21TZYPBua7NGDuqqbtqCfH8nUJ1RYfzwZPFS9TXkw'
#     access_token = '961922306464534528-Hvt4QShRMfSOVtk4gWDIQYQKxn4Hzeu'
#     access_secret = '6JlD4bU3Wplq81nJfyyJAwqsS1zgHZJEjBa8IPtKOBhmV'
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_secret)
#     api = tweepy.API(auth)
#     return api


consumer_key = 'btajWcCdHsqGckzWKg8cT42Ss'
consumer_secret = '3A9bzg07e21TZYPBua7NGDuqqbtqCfH8nUJ1RYfzwZPFS9TXkw'


# def get_access_tokens(request):
#     url = 'https://twitter.com/pythonsweng?oauth_token=9gGFngAAAAAA4twUAAABYpr4zxQ&oauth_verifier=fTn453QiYOWVJNex96D03AGDDmKDy6Du'
#     parsed = urlparse.urlparse(url)
#     # print (urlparse.parse_qs(parsed.query)['oauth_token'])
#     # print (urlparse.parse_qs(parsed.query)['oauth_verifier'])


def setTwitterAuth():
    # below two parameters will be set by the app developers only once
    consumer_key = 'btajWcCdHsqGckzWKg8cT42Ss'
    consumer_secret = '3A9bzg07e21TZYPBua7NGDuqqbtqCfH8nUJ1RYfzwZPFS9TXkw'
    # <below to parameters will be different for every single user that uses our bot
    access_token = '961922306464534528-Hvt4QShRMfSOVtk4gWDIQYQKxn4Hzeu'
    access_secret = '6JlD4bU3Wplq81nJfyyJAwqsS1zgHZJEjBa8IPtKOBhmV'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api



# def setTwitterAuth():
#     consumer_key = '	tcrYJonfXQUMLvv2vCugCvpLm'
#     consumer_secret = 'ikLvlchhknKzGLN9h7Arwaf20EWeIzsF9eGp5v0fGabWUfCQIS'
#     access_token = '	961922306464534528-AW3IVtqCtosIieiFXIAvRq3OOtmiOCe'
#     access_secret = 'rfISXOhL8LqatouHHZ94BtBPjkASrzQ1Uzk6kw3ewiWBv'
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_secret)
#     api = tweepy.API(auth)
#     return api



def authorize(request):
    consumer_key = 'btajWcCdHsqGckzWKg8cT42Ss'
    consumer_secret = '3A9bzg07e21TZYPBua7NGDuqqbtqCfH8nUJ1RYfzwZPFS9TXkw'

    # consumer_key = 'XUWkLPT3VDojtTsQENapNdV4f'
    # consumer_secret = 'Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP'
    # consumer_key = input('consumer key ').strip()
    # consumer_secret = input('consumer secret ').strip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Open authorization URL in browser
    webbrowser.open(auth.get_authorization_url())

    # Ask user for verifier pin
    pin = input('Verification pin number from twitter.com: ').strip()

    # Get access token
    token = auth.get_access_token(verifier=pin)

    # Give user the access token
    print ('Access token:')
    print ('  Key: %s' % token[0])
    print (' Secret: %s' % token[1])



# if __name__ == '__main__':
#     authorize()




 # Key: 981884988709851137-C3n9IYuIRG4nVxRH5adkjLuK37em6LV
 # Secret: x9Dgfjg28GvY8wAhqaCJVFnnOXfRe5FhejIcYjnPvMivY

#
# def verification(request):
#     consumer_key = 'XUWkLPT3VDojtTsQENapNdV4f'
#     consumer_secret = 'Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP'
#     # consumer_key = input('XUWkLPT3VDojtTsQENapNdV4f').strip()
#     # consumer_secret = input('Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP').strip()
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     # Open authorization URL in browser
#     webbrowser.open(auth.get_authorization_url())
#
#
#     # Ask user for verifier pin
#     pin = str(input('Verification pin number from twitter.com: '))
#
#     # Get access token
#     token = auth.get_access_token(verifier=pin)
#
#     # Give user the access token
#     print ('Access token:')
#     print (' Key: %s' % token[0])
#     print ('Secret: %s' % token[1])
#     access_token = token[0]
#     access_secret = token[1]
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_secret)
#     api = tweepy.API(auth)
#     api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#     return api



# def verifier(request):
#     consumer_key = 'XUWkLPT3VDojtTsQENapNdV4f'
#     consumer_secret = 'Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP'
#     twitter = OAuthHandler(consumer_key, consumer_secret)
#     request_token = twitter.getRequestToken()




# Mursaleen _app
    # consumer key= URCTNLThkHQAxCFLtMjWOnMlA
    # consumer_secret = lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y

# Top of the floor
# consumer_key = 'XUWkLPT3VDojtTsQENapNdV4f'
# consumer_secret = 'Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP'


def auth(request):
    consumer_token = 'XUWkLPT3VDojtTsQENapNdV4f'
    consumer_secret = 'Dihixu6byI8KQj2mQGcrI4W7fwFHKnDLAUPw4082xxH85QKLbP'
    callback_url = 'http://127.0.0.1:8000/home_page/'
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    url = auth.get_authorization_url()

    return redirect( url )




def verification(request):
    redirect_url = ''
    consumer_key = 'URCTNLThkHQAxCFLtMjWOnMlA'
    consumer_secret = 'lVQoh3ywFUeGSzMYkXjyA3g3kYHMpkrRpiX8ccfrvVmSKvJr7y'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    try:
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] =  auth.request_token

    except tweepy.TweepError:
        print('Error! Failed to get request token.')


    return redirect(redirect_url)