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
followers_list = []
for x in followers['users']:
  user = {}
  user['name'] = x['name']
  user['screen_name'] = x['screen_name']
  user['image_url'] = x['profile_image_url_https']
  user['false_percent'] = 0
  user['profile_text'] = x['description']
  user['followers_count'] = x['followers_count']
  followers_list.append(user)
  
for u in followers_list:
  same_names = t.users.search(q=u['name'],count=5)
  same_names = sorted(same_names, key=lambda x:x["followers_count"],reverse=True)

  for s in same_names:
    if u['name'] == s['name']:
      same_name = s
      break
  print(same_name['name'])
  #for y in same_names:
  if u['name']==same_name['name']:
    if u['screen_name']==same_name['screen_name']:
      print('  ' + u['name'] + '@' + u['screen_name'] + " " + str(u['followers_count']) + " [本物]")
    else:
      print('  ' + same_name['name'] + '@' + same_name['screen_name'] + " " + str(same_name['followers_count']) + " [本物?]")
      print('  ' + u['name'] + '@' + u['screen_name'] + " " + " [偽物かも?]")
      print("  -> 画像判別：　未実装")
      u['false_percent']  = u['false_percent'] + Word.wordCompare(u['profile_text'],same_name['description'])
      print("  -> 文字判別：　" + str(u['false_percent']) + "%")
      print("  -> その他：　未実装")
  print('---------------------------------------------------')
  pass
#print(followers_list)

