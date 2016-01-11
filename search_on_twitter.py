# -*- coding: utf-8 -*-
#
# Library: 
#   https://github.com/sixohsix/twitter
#
# Twitter Search API
#   https://dev.twitter.com/rest/public/search
#   https://dev.twitter.com/rest/reference/get/search/tweets
#
# Twitter API Limits
#   450 queries per 15 minute for seach api
#   https://dev.twitter.com/rest/public/rate-limiting
# 
import json
from twitter import *
import Word



# OAuth2.0用のキーを取得する
with open("secret.json") as f:
    secretjson = json.load(f)

# Twitterへの接続
t = Twitter(auth=OAuth(secretjson["access_token"], secretjson["access_token_secret"], secretjson["consumer_key"], secretjson["consumer_secret"]))

# 検索する
followers = t.followers.list(screen_name="@haru_python", count=50)
for x in followers['users']:
  print(x['name'] + '@' + x['screen_name'])
  print('tweet:' + str(x['statuses_count']))
  print('follows:' + str(x['friends_count']))
  print('followers:' + str(x['followers_count']))
  print('following:' + str(x['following']))     
  same_names = t.users.search(q=x['name'],count=5)
  same_names = sorted(same_names, key=lambda x:x["followers_count"],reverse=True)
  for y in same_names:
    if x['name']==y['name']:
      if x['screen_name']==y['screen_name']:
        print('  ' + y['name'] + '@' + y['screen_name'] + " " + str(y['followers_count']) + " [本物]")
      else:
        print('  ' + y['name'] + '@' + y['screen_name'] + " " + str(y['followers_count']) + " [本物?]")
        print('  ' + x['name'] + '@' + x['screen_name'] + " " + str(x['followers_count']) + " [偽物かも?]")
        print("  -> 画像判別：　未実装")
        print("  -> 文字判別：　" + Word.wordCompare(x['description'],y['description']))
        print("  -> その他：　未実装")
  print('---------------------------------------------------')
  pass

