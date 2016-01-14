import MeCab
mecab = MeCab.Tagger ("-Ochasen")

def wordCompare(word1,word2):
  if word1==word2:
    return 100
  else:
    w_list1 = mecab.parse(word1)
    w_list2 = mecab.parse(word2)
    word_group1 = set(trim(w_list1)).difference([",",".","、","。"])
    word_group2 = set(trim(w_list2)).difference([",",".","、","。"])
    match_count = len(word_group1.intersection(word_group2))
    print("Count" + str(match_count))
    if match_count == 2:
      return 10
    elif match_count == 3:
      return 30
    elif match_count == 4:
      return 50
    elif match_count >= 5:
      return 60
    else:
      return 0

def trim(words):
  n_word_list = []
  word_list = words.split("\n")
  for w in range(len(word_list)):
    #print("|||" + word_list[w])
    if "EOS" == word_list[w]:
      break
    else:
      c1 = word_list[w].split("\t")
      if "名詞" in word_list[w] and "名詞" in word_list[w-1] and "記号" not in word_list[w] and "記号" not in word_list[w-1] and "," not in word_list[w] and "," not in word_list[w-1]:

        c2 = word_list[w-1].split("\t")
        if c2[0] in n_word_list[len(n_word_list)-1]:
          n_word_list[len(n_word_list)-1] = n_word_list[len(n_word_list)-1] + c1[0]
        else:
          n_word_list[len(n_word_list)-1] = c2[0] + c1[0]
      elif "名詞" in c1[3]:
        n_word_list.append(c1[0])
  print(n_word_list)
  return n_word_list

