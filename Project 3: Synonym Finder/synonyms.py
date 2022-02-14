'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    m1=0
    m2=0
    num=0

    for key in vec1:
        if key in vec2 :
            num+=vec1[key]*vec2[key]    #the sum of the multiple of common dictionary keys for vec1 and vec2
        m1+=math.pow(vec1[key],2)    #the sum of the square of all values in vec1

    for key in vec2:
        m2+=math.pow(vec2[key],2)    #the sum of the square of all values in vec2

    denom=math.sqrt(m1*m2)    #the denominator which is the sqrt of the multiple of m1 and m2.
    return num/denom                # for vec1={"a": 1, "b": 2, "c": 3}, vec2={"b": 4, "c": 5, "d": 6}: ans=0.70052


def build_semantic_descriptors(sentences):
    ans={}
    for sentence in sentences:     #extract sentences
        sentdic={}                   #initialize sentence dictionary
        for keyword in sentence:       #loop through sentence and extract keys
            if(keyword not in sentdic):  #check that the keyword has not already been added to sentdic
                sentdic[keyword]={}        #add keyword to dictionary
                for word in sentence:        #loop through sentence to add words and counts to sentdic[keyword]
                    if(word!=keyword):         #check that the word is not the keyword (cant associate key with itself)
                        if(word not in sentdic[keyword]):  #check that this word is unique/not the key
                            sentdic[keyword][word]=1       #add word to keyword dict and initailize by giving vaue 1
                        else:                              #other cases are when it is in the dictionary already
                            sentdic[keyword][word]+=1      #increase count for that word
        for key in sentdic:      #loop through keys in sentence dictionary
            if key in ans:            #find if key is in answer dict
                for word in sentdic[key]:  #loop through words in key
                    if(word not in ans[key]):   #check if word is not in key
                        ans[key][word]=sentdic[key][word]  #add word to ans
                    else:                                  #in other case, word is in ans
                        ans[key][word]+=sentdic[key][word] #add word count to ans
            else:                      #if key is not in ans run this:
                ans[key]=sentdic[key]  #add all words and key to ans
    return ans                         #return dictionary of word dictionarys






def build_semantic_descriptors_from_files(filenames):
    sentences=[]              #initializes list that will hold sentince list
    replace=[",", "-", "--", ":", ";"]      #list of stuff to remove from any passage
    for file in filenames:                              #loop through files
        current=open(file, "r", encoding="latin1").read().lower()   #open file, make string and make it lowercase
        for s in replace:                   #loop through symbols in replace
            current.replace(s,"")           #replce the symbol in current with ""
        hold=[]                             #initiate a sentence list
        current=current.split()             #split current into a list of words
        for word in current:                #loop through words
            if(word.find(".")!=-1 or word.find("!")!=-1 or word.find("?")!=-1):   #find end of sentinces
                hold.append(word[0:len(word)-1])                                #add word minus period to hold
                sentences.append(hold)                                        #add hold to sentences
                hold=[]                                                     #make hold empty
            else:                                                         #otherwise it isnt the end of the sentence
                hold.append(word)                                       #add word to hold
    return build_semantic_descriptors(sentences)                      #the semantic descriptors of sentences are returned



def most_similar_word(word, choices, semantic, fn):
    ans=choices[0]             #initiate answer with first index of choises incase they all are not in semantic
    max=-1                     #set max to the min possible value
    if(word not in semantic):  #if word isnt in semantic it cant be compared so -1 case is returned
        return ans             #return simple case

    for choise in choices:              #loop through all choises
        if(choise in semantic):                  #check that the choice is in semantic and thus comparable
            if(max<fn(semantic[word],semantic[choise])):  #checks if choice is more similar than ans
                max=fn(semantic[word],semantic[choise])   #records similarity as max
                ans=choise                                #updates ans
    return ans                                            #return ans once all choices have been analized


def run_similarity_test(file, semantic, fn):
    correct=0                                  #initialize counter for correct answers
    a_file=open(file, "r", encoding="latin1")  #extract test cases contained in file
    cases=[]                                   #initialize cases list
    for line in a_file:                        #loop through lines in fine to extract cases
        stripped_line = line.strip()           #take out \n and separate
        line_list = stripped_line.split()      #isolate each line as a list
        cases.append(line_list)                          #append each test case to cases
    for case in cases:                                             #loop through test cases
        if(most_similar_word(case[0],case[2:] , semantic, fn)==case[1]):     #check if function return correct answer
            correct +=1                                                      #if yes add one to count
    return 100.0*correct/len(cases)                                          #return % of corect answers








if __name__ == '__main__':


    teststring=[["i", "am", "a", "sick", "man"],["i", "am", "a", "spiteful", "man"],["i", "am", "an", "unattractive", "man"],["i", "believe", "my", "liver", "is", "diseased"],["however", "i", "know", "nothing", "at", "all", "about", "my","disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]

    print(build_semantic_descriptors(teststring))
    files=["Notes_Underground.txt","Pride and Prejudice.txt","Swann's Way, by Marcel Proust.txt"]
    test="test.txt"
    semantic=build_semantic_descriptors_from_files(files)
    ans=run_similarity_test(test, semantic, cosine_similarity)
    print(ans)
    print(cosine_similarity(semantic["vexed"],semantic["annoyed"]))
    print(cosine_similarity(semantic["vexed"],semantic["amused"]))
    print(most_similar_word("vexed", ["annoyed", "amused"], semantic, cosine_similarity))
    #vexed annoyed amused









































