from django.shortcuts import render
import tweepy
import sys, requests, json, time, os
from django.contrib.messages.views import messages
from .forms import InputForm
from django.conf import settings


CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)



def unfollowers(request):
    form = InputForm()
    if request.method == "POST":
        try:
            form = InputForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['user_input']
                starttime = time.time()
                user = api.get_user(username)
                user_id = user._json['id']
                followed_users_ids = api.friends_ids(user_id)
                followers_ids = api.followers_ids(user_id)
                difference_list = diff(followed_users_ids, followers_ids)
                counter = 0
                counter_2 = 0
                a = []
                for i in range(len(difference_list)//100+1):
                    counter = i*100
                    counter_2 += 100
                    a.append(api.lookup_users(difference_list[counter:counter_2]))
                nons_list = []
                for i in a:
                    for j in i:
                        nons_list.append(j._json['id'])

                unfollowers_ids_list =list(set(nons_list) - set(followers_ids))
                counter_3 = 0
                counter_4 = 0
                b=[]
                for i in range(len(unfollowers_ids_list)//100+1):
                    counter_3 = i*100
                    counter_4 += 100
                    b.append(api.lookup_users(unfollowers_ids_list[counter_3:counter_4]))
                unfollowers_list = []
                times = time.time()-starttime
                for i in b:
                    for j in i:
                        unfollowers_list.append(j._json['screen_name'])
                    return render(request, 'twitter_bot/nonfollowers.html', {'form':form, 'unfollowers_list':unfollowers_list, 'times':times})
            
        except tweepy.error.TweepError:
            messages.error(request,'Bu kullanıcı adına sahip birisi yok')
            return render(request,'twitter_bot/nonfollowers.html', {'form':form})
         
    return render(request,'twitter_bot/nonfollowers.html',{'form':form})

def diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

     
