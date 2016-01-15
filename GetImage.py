import urllib.request, os

def saveImage(url,i_name, address):
  #OpenerDirectorオブジェクト生成
  opener = urllib.request.build_opener()
  #オープン
  httpres = opener.open(url)
  #print(httpres.getheaders()) #debug
 
  #ファイルサイズ
  sz = int(httpres.getheader('Content-Length'))
 
  #取得
  b = httpres.read()
 
  #保存先パス
  save_file = os.path.join(address, i_name)
  #保存
  with open(save_file, 'wb') as fpw:
    fpw.write(b)
