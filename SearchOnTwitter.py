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
import Image
#import urllib
import urllib.request, os
import sqlite3

db = sqlite3.connect('./db/users.db')
cursor = db.cursor()

sql_create = " ".join((
          "CREATE TABLE followers (",
          "user_name text,",
          "screen_name text,",
          "image_url text,",
          "false_percent integer,",
          "profile_text text,",
          "followers_count integer,",
          "profile_image binary",
          ");"))
sql_insert_f = " ".join((
                "INSERT INTO followers (",
                "user_name,",
                "screen_name,",
                "image_url,",
                "false_percent,",
                "profile_text,",
                "followers_count,",
                "profile_image",
                ") VALUES (?,?,?,?,?,?,?);"))
cur = db.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % "followers")
if cur.fetchone()==None:  #存在してないので作る
  cursor.execute(sql_create)
  db.commit()
else:
  cursor.execute("""DROP TABLE %s;""" % "followers")  #リセット
  cursor.execute(sql_create)

# OAuth2.0用のキーを取得する
with open("secret.json") as f:
    secretjson = json.load(f)

# Twitterへの接続
t = Twitter(auth=OAuth(secretjson["access_token"], secretjson["access_token_secret"], secretjson["consumer_key"], secretjson["consumer_secret"]))

my_account = input('あなたのアカウント名>>>  @')
my_account = "@" + my_account
print(my_account)
# 検索する
try:
  followers = t.followers.list(screen_name=str(my_account), count=50)
except:
  print("ERROR!!")
  exit()
  
followers_list = []
for x in followers['users']:
  user = {}
  user['name'] = x['name']
  user['screen_name'] = x['screen_name']
  user['image_url'] = x['profile_image_url_https']
  user['false_percent'] = 0
  user['profile_text'] = x['description']
  user['followers_count'] = x['followers_count']
  Image.saveImage(user['image_url'], user['screen_name'], "./pictures/followers")
  followers_list.append(user)
  
for u in followers_list:
  same_names = t.users.search(q=u['name'],count=50)
  same_names = sorted(same_names, key=lambda x:x["followers_count"],reverse=True)
  same_name = u
  for s in same_names:
    if u['name'] == s['name']:
      same_name = s
      break
  print("[ユーザー名] " + u['name'])
  
  
  if u['name']==same_name['name']:
    if u['screen_name']==same_name['screen_name']:
      print('  [アカウント名] ' + u['name'] + '@' + u['screen_name'] + " " + str(u['followers_count']) + " [本物]\n")
      cursor.execute(sql_insert_f,(u['name'], u['screen_name'], u['image_url'], 0, u['profile_text'], u['followers_count'], None)) 
    else:
      print('  [アカウント名] ' + same_name['name'] + '@' + same_name['screen_name'] + " " + str(same_name['followers_count']) + " [本物?]")
      print('  [アカウント名] ' + u['name'] + '@' + u['screen_name'] + " " + str(u['followers_count']) + " [偽物かも?]")
      ######## 画像比較 ########
      print("  -> 画像判別:  ")
      Image.saveImage(same_name['profile_image_url_https'], same_name['screen_name'], "./pictures/same_name_users")
      image_match = Image.compareImage(u['screen_name'], same_name['screen_name'])
      print("    画像類似度" + str(image_match) + "%")
      u['false_percent']  = u['false_percent'] + image_match
      
      ######## 文字比較 ########
      print("  -> 文字判別:  ")
      word_match = Word.wordCompare(u['profile_text'],same_name['description'])
      u['false_percent']  = u['false_percent'] + word_match
      print("    プロフィール類似度: " + str(word_match) + "%")
      
      print("  -> その他:  未実装")

      print("なりすましアカウント率: " + str(u['false_percent']) + "%\n")
      cursor.execute(sql_insert_f,(u['name'], u['screen_name'], u['image_url'], u['false_percent'], u['profile_text'], u['followers_count'], None))

  print('---------------------------------------------------')
  pass
db.commit()
db.close()
#print(followers_list)



