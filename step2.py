from itertools import groupby
import re
import main
from collections import Counter, defaultdict

##task1
##Assign1 output a txt document that contain all words named words.txt, Read the txt
f=main.readToken("./words.txt"," ")
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


new_list=split_list(f)
#delete ###that we generated
counts = Counter(f)
counts_dict = dict(counts)
for key in counts_dict:
    if pattern.match(key) in counts_dict: del counts_dict['key']

#print inverted index
corpus=list(counts_dict.keys())
index=inv(corpus,new_list)
print(index)



##task2



def merge_dictionaries(dict1, dict2):
    """
       merged_dictionary<dictionary> Returns a dictionary that merged two dictionaries together

       Parameter:
           dict1,dict2:the dictionaries that need to merge

    """
    merged_dictionary = {}

    for key in dict1:
        if key in dict2:
            new_value = dict1[key] + dict2[key]
        else:
            new_value = dict1[key]

        merged_dictionary[key] = new_value

    for key in dict2:
        if key not in merged_dictionary:
            merged_dictionary[key] = dict2[key]

    return merged_dictionary

# keep asking to input str or list and find the key word in inverted index taht we created
loop=1
while loop==1:
    list_dic={}
    kw=str(input("plz input a str/list,press enter as the end")).lower()
    if kw=="#":
        loop=0
    else:
        search_list = kw.split(' ')
        search_list=list(set(search_list))
        for word in search_list:
            if word not in corpus:
                search_list.remove(word)
            else:
                list_dic[word]=index[word]
#count the frequency
        scores=dict()
        for words in search_list:
            for k in index[words]:
                k_id,count=list(k.items())[0]
                if k_id not in scores:
                    scores[k_id]=0
                scores[k_id]+=count


        top=Counter(scores).most_common(10)
        print(top)
    if loop ==0:
        break






