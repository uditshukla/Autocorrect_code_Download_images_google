import json
import os
import re
import sys

import nltk
import yaml

from gingerit.gingerit import GingerIt
from elasticsearch import Elasticsearch
from nltk import tokenize
newSentence = None

with open("../config.yml", 'r') as yml_file:
    cfg = yaml.load(yml_file)

directory = cfg['root']
dict_index_name = cfg['elasticSearch']['dict_index_name']
word_map_index= cfg['elasticSearch']['word_map_index']
es_host = cfg['elasticSearch']['host']
es_port = cfg['elasticSearch']['port']

simple_search_query = cfg['query']['simple_search_query']
fuzzy_search_query =  cfg['query']['fuzzy_search_query']
mappingQuery = cfg['query']['mapping_query']
es = Elasticsearch([{'host': es_host, 'port': es_port}])


def correct_sentence_autometa(_sent):
    parser = GingerIt()
    processed = parser.parse(_sent)
    return processed
    # print(processed['result'])


def soundex(query: str):
    """
    https://en.wikipedia.org/wiki/Soundex
    :param query:
    :return:
    """

    # Step 0: Clean up the query string
    query = query.lower()
    letters = [char for char in query if char.isalpha()]

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If query contains only 1 letter, return query+"000" (Refer step 5)
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Step 3: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind + 1 < len(letters) and char != letters[ind + 1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 5: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string


def get_levenshtein_distance(word1, word2):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    :param word1:
    :param word2:
    :return:
    """
    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    print(matrix)


def get_levenshtein_distance(word1, word2):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    :param word1:
    :param word2:
    :return:
    """
    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    for x in range(1, len(word1) + 1):
        for y in range(1, len(word2) + 1):
            if word1[x - 1] == word2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )

    return matrix[len(word1)][len(word2)]


def extractText(filepath):
    from xml.etree import cElementTree as ET
    with open(filepath, 'r') as file:
        data = file.read()
        # print(data)
    root = ET.fromstring(data)
    str = ""
    for page in list(root)[5]:
        content = page.find('text')
        # print(content.text.strip())
        str += content.text.strip() + "\n"
    return str


def stripPunc(wordList):
    """Strips punctuation from list of words"""
    puncList = [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", "\""]
    for punc in puncList:
        for word in wordList:
            wordList = [word.replace(punc, '') for word in wordList]
    return wordList


def count_letter(word, char):
    count = 0
    for c in word:
        if c == char:
            count += 1
    return count


def word_mapping_check(txt):
    import re
    paragraph = txt
    allKey = es.search(index=word_map_index, body=mappingQuery)
    allkeyJson = allKey['hits']['hits']
    for key in allkeyJson:
        if key['_id'] in paragraph:
            print("Suggested: " + key['_id'] + ">>" + key['_source']['properword'])
        paragraph = re.sub(key['_id'], key['_source']['properword'], paragraph)
    return paragraph


def include_apostrophe_words_es(apostrophe):
    m = {'world': apostrophe.replace("'", "\'")}
    n = json.dumps(m)
    o = json.loads(n)
    try:
        es.index(index=dict_index_name, doc_type='doc', body=o, id=apostrophe.replace("'", "\'"))
    except Exception as e:
        print(sys.exc_info()[0])


def breakRNA(seqRNA, *breakPoint):
    seqRNAList = []
    noOfBreakPoints = len(breakPoint)
    for breakPt in range(noOfBreakPoints):
        for index in breakPoint:
            seqRNAList.append(seqRNA[:index])
            seqRNA = seqRNA[index:]
        break
    return seqRNAList


def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]


def upper_word_intersect(infected_element):
    start_ixd = -1
    pattern_regex = re.compile("[A-Z]")
    if any(map(str.isupper, infected_element)):
        if not infected_element[0].isupper() and ' ' not in infected_element:
            while True:
                m = pattern_regex.search(infected_element, start_ixd + 1)
                if m is None:
                    break

                start_ixd = m.start()
                if ' ' not in infected_element:
                    corrected_element = insert_space(infected_element, start_ixd)
                    print(corrected_element)
                    return corrected_element
        if infected_element[0].isupper() and ' ' not in infected_element and (
        pattern_regex.search(infected_element, start_ixd + 1)) is not None:
            count2 = 0
            globalcount = 0
            count1 = 0
            for i in infected_element:
                count1 +=1
                if i.isupper():
                    count2 = count2 + 1
                    if count2 == 2:
                        globalcount = count1

            if count2 == 2:
                corrected_element = insert_space(infected_element,globalcount-1)
                print('----', corrected_element)
                return corrected_element

    # upper letter inside word string bug fix


def remove_correct_nltk(article):
    global non_noun
    tagged_sentence = nltk.tag.pos_tag(article.split())
    edited_sentence = [word for word, tag in tagged_sentence if tag != 'NNPS'
                       and tag != 'PRP' and tag != 'VBP' and tag != 'DT' and tag != 'PRP$' and tag != 'CC' and tag != 'MD'
                       and tag != 'IN' and tag != 'TO']
    non_noun = (' '.join(edited_sentence))
    return non_noun


# code starts here ##
def main():
    global world
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            print('--------------------------------------------------')
            print(os.path.join(directory, filename))
            print('--------------------------------------------------')
            sentences = extractText(directory + filename)
            #sentences = 'th e'
            article = word_mapping_check(sentences.replace('-\n', '').replace('\n', ''))
            non_noun = remove_correct_nltk(article)

            for sentences in tokenize.sent_tokenize(non_noun):
                worldsList = stripPunc(sentences.split())
                bigram = list(nltk.bigrams(nltk.word_tokenize(non_noun)))
                for element in worldsList:
                    # upper letter inside word string bugfix
                        searchQuery = str.replace(simple_search_query, "#WORD", str.lower(element))
                        rest = es.search(index=dict_index_name, body=searchQuery)
                        count = len(rest['hits']['hits'])
                        if count < 1:
                            for word in bigram:
                                wordCombine = ''.join(word)
                                if wordCombine.startswith(element):
                                    searchQuery = str.replace(simple_search_query, "#WORD", str.lower(wordCombine))
                                    rest = es.search(index=dict_index_name, body=searchQuery)
                                    count = len(rest['hits']['hits'])
                                    if count == 1:
                                        print("Bi-gram Suggested: ", ' '.join(word), '---->', wordCombine)
                                        re.sub(' '.join(word), wordCombine, article)
                                        article = article.replace(' '.join(word), wordCombine)
                                        bigram.pop(bigram.index(word))
                                        break

                            new_element = upper_word_intersect(element)
                            if element != '' and element is not None and new_element is not None:
                                article = article.replace(str(element), str(new_element))
                                if "'" in element:
                                    include_apostrophe_words_es(element)

                for world in worldsList:
                    world = world.replace('.', '').replace(',', '').replace('-', '')
                    searchQuery = str.replace(simple_search_query, "#WORD", str.lower(world))
                    rest = es.search(index=dict_index_name, body=searchQuery)
                    total = len(rest['hits']['hits'])
                    if total < 1:
                        searchQuery = str.replace(fuzzy_search_query, "#WORD", str.lower(world))
                        rest = es.search(index=dict_index_name, body=searchQuery)
                        data = [doc for doc in rest['hits']['hits']]
                        for doc1 in data:
                            processed_fuzzy = doc1['_source']['word']
                            ld = get_levenshtein_distance(str.lower(world), str.lower(processed_fuzzy))
                            if 3 >= ld > 0:
                                if soundex(world) == soundex(processed_fuzzy):
                                    print("Fuzz Suggested: ", world, '--->', processed_fuzzy)
                                    re.sub(world, processed_fuzzy, article)
                                    article = article.replace(world, processed_fuzzy)

            print("Corrected Article: " + article)
            continue
        else:
            continue


if __name__ == '__main__':
    main()
