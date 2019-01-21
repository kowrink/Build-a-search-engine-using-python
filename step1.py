import os
import string
import re
from collections import Counter

def strclear(text):
    """
       Strings(str) Returns strings that contain all elements in the
       list and make sure there are spaces between them

       Parameter:
           text (list): The list of the words
    """
    text = ''.join(text)
    text =  re.sub('\s+', ' ', text)
    msg = ''.join(text)
    return msg

def write_file():
    """

       Read all files in the dataset floder and write all the words they contain down
       in a new file called words.txt

    """
    path = "dataset\cranfieldDocs"
    files= os.listdir(path)
    length=0
    new_file= open("words.txt","w+")

    # read each word in each line in each file
    for file in files:
        f=open(path+"/"+file, 'r')
        strs=''
        for line in f:
            tokens=re.split("[^a-z0-9]",line)
            for char in tokens:
                strs = strs + char+" "
        strs = strclear(" ".join(strs.split()))
        strs = strs + " "


    # join the words list into strings and write it in the file "words"

        length=length+len(strs.split())
        new_file.write("###")
        new_file.write(strs)
    new_file.close()
    f.close()


def readToken(path,dot):
    """
       list<list> Returns a list that contain all elements in the given file

       Parameter:
           path (str): The path of the file
           dot(str): What symbol the file using to split words
    """
    with open(path, 'r') as f:
        f1= f.readline().split(dot)
        return f1

def summary(path,dot,file_name):
    """
       Create three new files to answer three questions:
       a: total words number
       b: words size
       c: Top 50 words

       Parameter:
           path(str): the file that need to read
           dot(str): the symbol used to split
           file(str): the file name that need to create
       """
    tokens = readToken(path,dot)
    length=0
    words_size=0
    sum_file = open(file_name, "w+")
    counts = Counter(tokens)

    # transfer counter into dictionary and count the frequency of each word to get the size and total length
    counts_dict=dict(counts)
    for k, v in counts_dict.items():
        length=length+int(v)
        words_size = words_size+1
    sum_file.write("\nlength (question a) \r\n"+ str(length)+"\r\n")
    sum_file.write("Unique size (question b) \r\n " + str(words_size) + "\r\n")

    # use counter function to get the most frequent 50 words
    sum_file.write("TOP 50 (question c) \r\n" )
    for k, v in counts.most_common(50):
        sum_file.write("{} {}\n".format(k, v))
    sum_file.close()


def delete_words():
    """
       Create a new file to record the words without common words

    """
    with open("./dataset/common_words.txt") as f1:
        content = f1.readlines()
    f1 = [x.strip() for x in content]
    f2=readToken("./words.txt"," ")
    delete_file = open("delete.txt", "w+")
    # only take the words that not in common words into the delete.txt
    for chars in f2:
        if chars not in f1:
           delete_file.write(" "+ chars)
    delete_file.close()


def main():
    """
       Main function,to use the function above to create files that record all the words
       and words without common words respectively and compare their total words,size and top
       50 words
    """
    write_file()
    summary("words.txt"," ","task1.txt")
    delete_words()
    summary("delete.txt", " ", "task2.txt")


if __name__ == '__main__':
    main()

















