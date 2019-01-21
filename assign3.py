from collections import Counter
import re
import math
import operator
import timeit


# from prettytable import PrettyTable
##The word.txt use "###" to seperate meterials in different files
pattern = re.compile('^###.')


def inv(corpus_dict,docs):
    """
       list<list> Returns a list that contain all introverted index

       Parameter:
           corpus_dict: the corpus that contain all words
           docs: the list that contain all the documents
    """
    inv_indx = {i:[] for i in corpus_dict}
    for word in corpus_dict:
        for i in range(len(docs)):
            if word in docs[i]:
                fre=dict(Counter(docs[i])).get(word)
                inv_indx[word].append({i+1:fre})

    return inv_indx

def readToken(path, dot):
    """
       list<list> Returns a list that contain all elements in the given file

       Parameter:
           path (str): The path of the file
           dot(str): What symbol the file using to split words
    """
    with open(path, 'r') as f:
        f1 = f.readline().split(dot)
        return f1


def cosine(l1, l2):
    """
       int: Returns  cosine of L1 and L2

       Parameter:
           L1,L2: The list that need to calculate cosine
    """
    Mutiply_list = sum([a * b for a, b in zip(l1, l2)])
    sum1 = 0.0001
    sum2 = 0.0001
    for element in l1:
        ele_sqr1 = element ** 2
        sum1 += ele_sqr1
    for element in l2:
        ele_sqr2 = element ** 2
        sum2 += ele_sqr2
    outcome = Mutiply_list / math.sqrt(sum1 * sum2)
    return outcome


def split_list(L):
    """
       list<list> Returns a lists of a individual documents

       Parameter:
           L:the list that need to split, using ### to seperate files meterials
    """
    Lsub = []
    L2 = []
    for e in L:
        if pattern.match(e):
            if Lsub:
                L2.append(Lsub)
            Lsub = [e]
        else:
            Lsub.append(e)
    L2.append(Lsub)
    return L2


dic_file = open("dic.txt", "w+")
mat_file = open("mat.txt", "w+")
tokens = readToken("words.txt", " ")
deleted_common = readToken("delete.txt", " ")
counts = Counter(deleted_common)
most_1000 = counts.most_common(1000)
most_1000 = list(dict(most_1000).keys())
new_list = split_list(tokens)
dic = {}

counts = Counter(tokens)
counts_dict = dict(counts)
for key in counts_dict:
    if pattern.match(key) in counts_dict: del counts_dict['key']

#caculate inverted index
corpus=list(counts_dict.keys())
index=inv(corpus,new_list)

#calculate idf
for words in most_1000:
    t = [0] * 1400
    i = 0
    for doc in new_list:
        if words in doc:
            t[i] = 1
        i += 1
    dic_temp = {words: t}
    dic.update(dic_temp)
sum_list = []
for common_words in dic.keys():
    s = sum(dic[common_words])
    sum_list.append(s)
idf = [math.log2(1400 / i) for i in sum_list]


#calculate tf-idf
k = 1
dic2 = {}
i=1
for doc in new_list:
    freq_list=[]
    for words in most_1000:
        if words not in doc:
            freq=0
        else:
            freq=(dict(Counter(doc)).get(words))
        freq_list.append(freq)
    dic_temp={i:freq_list}
    dic2.update(dic_temp)
    i+=1


tf_idf = {}
for k in dic2.keys():
    k_tf = dic2.get(k)
    list_tf_idf = [a * b for a, b in zip(k_tf, idf)]
    temp_tf_idf = {k: list_tf_idf}
    tf_idf.update(temp_tf_idf)

for k, v in tf_idf.items():
    dic_file.write(str(k) + ' >>> ' + str(v) + '\n\n')


#keep asking user to input queries
loop = 1
while loop == 1:
    choice=int(input("plz input a number,enter # to quit,1,using vector space model;2,using inverted index"))
    if choice=="#":
        break
#Turn query into [0] or [1] form
    query = str(input("plz input a query"))
    query = query.split()
    query_sum = [0] * 1000
    for keyword in query:
        keyword_rank = most_1000.index(keyword)
        query_sum[keyword_rank] = 1

#Using vector spcae to search
    if choice==1:
        start = timeit.default_timer()
        dic_relevant = {}
        result = 0
        scores = []
        cosine_indx = []
        doc_no = 1
        for doc_no in range(1, 1400):
            values = tf_idf.get(doc_no)
            cosine_word = cosine(query_sum, values)

            dicr_temp={doc_no:cosine_word}
            dic_relevant.update(dicr_temp)

        a=dict(sorted(dic_relevant.items(), key=operator.itemgetter(1), reverse=True)[:10])
        stop = timeit.default_timer()


#Using inverted index to search
    else:
        start = timeit.default_timer()
        files_list=[]
        dic_relevant={}
        for keyword in query:
            if keyword in index.keys():
                for files in index[keyword]:
                    if files.keys not in files_list:
                        files_list.extend(files.keys())
        for index_file in files_list:
            values = tf_idf.get(index_file)
            cosine_word = cosine(query_sum, values)

            dicr_temp = {index_file: cosine_word}
            dic_relevant.update(dicr_temp)
        a = dict(sorted(dic_relevant.items(), key=operator.itemgetter(1), reverse=True)[:10])
        stop = timeit.default_timer()

    print(a)
    print('Time: ', stop - start)

#The file words.txt and delete.txt are generated in the assignment1. These two file is used here.
# The output is as below,using inverted index is much faster than using vector space model.
# C:\Users\11984\AppData\Local\Programs\Python\Python36\python.exe "C:/Users/11984/Desktop/Thewaytodatascientist/information retrieval/dataset/assign3.py"
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index2
# plz input a queryinformation
# {251: 0.34408166965938186, 1214: 0.31466081619035957, 36: 0.30487556155885415, 440: 0.27079422997927244, 1027: 0.2598878550016386, 906: 0.23056683185152782, 1334: 0.22668061783496213, 925: 0.2094460914919389, 41: 0.17885290725410377, 907: 0.17766198105317252}
# Time:  0.02681845053602029
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index1
# plz input a queryinformation
# {251: 0.34408166965938186, 1214: 0.31466081619035957, 36: 0.30487556155885415, 440: 0.27079422997927244, 1027: 0.2598878550016386, 906: 0.23056683185152782, 1334: 0.22668061783496213, 925: 0.2094460914919389, 41: 0.17885290725410377, 907: 0.17766198105317252}
# Time:  0.7157814499358146
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index1
# plz input a querymethod
# {473: 0.33826235343305006, 745: 0.2817976347197319, 756: 0.2588779503889697, 264: 0.2524398980032794, 91: 0.24997884401247866, 1375: 0.24927082373897141, 193: 0.24748478322326795, 234: 0.2436902029616146, 1248: 0.23457995435315598, 292: 0.2340000258017689}
# Time:  0.94523243272522
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index2
# plz input a querymethod
# {473: 0.33826235343305006, 745: 0.2817976347197319, 756: 0.2588779503889697, 264: 0.2524398980032794, 91: 0.24997884401247866, 1375: 0.24927082373897141, 193: 0.24748478322326795, 234: 0.2436902029616146, 1248: 0.23457995435315598, 292: 0.2340000258017689}
# Time:  0.26666368547125785
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index1
# plz input a querytransfer equations
# {872: 0.3473879099437642, 1366: 0.27218171856624784, 1185: 0.26724270821658275, 873: 0.26140394856259697, 305: 0.24960969192853036, 398: 0.24209475079579762, 274: 0.2404830568422125, 123: 0.23908819657145836, 936: 0.2362755796086494, 623: 0.23288597782766274}
# Time:  0.8838027143374347
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index2
# plz input a querytransfer equations
# {872: 0.3473879099437642, 1366: 0.27218171856624784, 1185: 0.26724270821658275, 873: 0.26140394856259697, 305: 0.24960969192853036, 398: 0.24209475079579762, 274: 0.2404830568422125, 123: 0.23908819657145836, 936: 0.2362755796086494, 623: 0.23288597782766274}
# Time:  0.3306095053910667
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index1
# plz input a queryfree problem case
# {2: 0.22792808530422737, 644: 0.2175257181172079, 1148: 0.21731899872907587, 404: 0.2090025795119299, 1201: 0.2042766624020988, 87: 0.1992596046376923, 732: 0.1991961712334821, 493: 0.19643979365079928, 571: 0.19491987910528602, 966: 0.19429427148873973}
# Time:  0.8778695885664547
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index2
# plz input a queryfree problem case
# {2: 0.22792808530422737, 644: 0.2175257181172079, 1148: 0.21731899872907587, 404: 0.2090025795119299, 1201: 0.2042766624020988, 87: 0.1992596046376923, 732: 0.1991961712334821, 493: 0.19643979365079928, 571: 0.19491987910528602, 966: 0.19429427148873973}
# Time:  0.44806176489782956
# plz input a number,enter # to quit,1,using vector space model;2,using inverted index