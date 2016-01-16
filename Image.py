import urllib.request, os
import cv2
import numpy as np
import pylab as plt
import numpy
import math

def saveImage(url,i_name, address):
  #OpenerDirectorオブジェクト生成
  opener = urllib.request.build_opener()
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


def compareImage(img1_name, img2_name):
  img1_adr = "./pictures/followers/" + img1_name
  img2_adr = "./pictures/same_name_users/" + img2_name
  #viewImage(img1_adr)
  #viewImage(img2_adr)
  img1 = cv2.imread(img1_adr) # 比較するImageFile
  img2 = cv2.imread(img2_adr) # 比較するImageFile
  img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  img1_bw = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  img2_bw = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

  img1_hist = cv2.calcHist(img1, [0], None, [256], [0, 256])
  img2_hist = cv2.calcHist(img2, [0], None, [256], [0, 256])
  
 #############################################
  # CV_COMP_CORREL 相関
  # CV_COMP_CHISQR カイ2乗
  # CV_COMP_INTERSECT 交差
  # CV_COMP_BHATTACHARYYA Bhattacharyya距離
  #############################################
  img_diff = cv2.absdiff(img1, img2)
  #img_diff_name = img1_name + "_" + img2_name + ".jpg"
  #cv2.imwrite(img_diff_name,img_diff)
  
  #image_bw = cv2.adaptiveThreshold(img_diff,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) 
  #img_diff_name = img1_name + "_" + img2_name + "2.jpg"
  #cv2.imwrite(img_diff_name,image_bw)


  print("    diff: " + str(cv2.countNonZero(img_diff)))
  #print("  " + str(cv2.countNonZero(image_bw) ))
  
  #print(numpy.nonzero(img_diff))

  result1=100-100/640*cv2.compareHist(img1_hist, img2_hist,1)
  result2=100/48*cv2.compareHist(img1_hist, img2_hist,2)
  result3=100-100*cv2.compareHist(img1_hist, img2_hist,3)
  result4=100-cv2.compareHist(img1_hist, img2_hist,4)/25.6
  print("    処理1: " + str(int(result1)) + "%")
  print("    処理2: " + str(int(result2)) + "%")
  print("    処理3: " + str(int(result3)) + "%")
  print("    処理4: " + str(int(result4)) + "%")
  result_fin = (result1*0.9+result2*1.1+result3*1.1+result4*0.9)/4
  #print("最終画像類似度: " + str(int(result_fin)) + "%")
  return int(result_fin) 
  
def viewImage(adr):
  im = cv2.imread(adr,flags=1)
  # print(adr)
  if im is None:
    print("None")
    exit()
  plt.imshow(im)
  plt.show()

"""
print(str(compareImage("cannottalk", "haruka"))+"  Not Equal")
print("-----------------------------------------------------")
print(str(compareImage("haruka_system", "OriishiTakahiro"))+"  Simillar")
print("-----------------------------------------------------")
print(str(compareImage("OriishiTakahiro", "OriishiTakahiro"))+"  Equal")
print("-----------------------------------------------------")
print(str(compareImage("white", "black"))+"  Max Not Equal")
print("-----------------------------------------------------")
print(str(compareImage("moryyy35", "OriishiTakahiro"))+"  Not Equal")
"""



