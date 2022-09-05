import util
import nltk
import operator
from nltk.stem import PorterStemmer

# https://blog.csdn.net/pengjian444/article/details/81143983 超链接为下面字符串的意思
type_cd = ['CD']
type_cc = ['CC']
type_in = ['IN']
type_to = ['TO']
type_jj = ['JJ', 'JJR', 'JJS']
type_nn = ['NN', 'NNS', 'NNP', 'NNPS']
type_rb = ['RB', 'RBR', 'RBS']
type_vb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
type_ky = ['KY']
type_all = type_cd + type_cc + type_in + type_to + type_jj + type_nn + type_rb + type_vb + type_ky


def query_parse(query, path_parsed_vocab, path_method_vocab):
    """


    :param query: 搜索内容
    :param path_parsed_vocab: 一个pkl文件的路径，内容为codebase(还是jdk？）中各个单词的频率
    :param path_method_vocab: 一个pkl文件的路径，内容为各个单词及其对应的数字组成的dict
    :return: 一个列表，其中每一个元素为[{query}中的一个单词或者使用频率最高的同义词替代，类型，重要性，在代码库中的频率]
    """
    vjdk = dict(util.load_pkl(path_parsed_vocab))
    vword = dict(util.load_pkl(path_method_vocab))
    stemmer = PorterStemmer()
    str_replace = ['in java', 'using java', 'java', 'how to', 'how do',
                   'what is']

    for str_re in str_replace:
        query = query.replace(str_re, '')

    data = []
    # 这里的query已经没有{str_replace}中的词汇了，将query分词，形成诸多关键词{tokens}
    tokens = util.get_tokens(query)
    # 识别查询分词后各个单词的属性，返回为列表，其中每一个元素为形式为('单词','类型')的元组
    tokens = nltk.pos_tag(tokens)

    for token in tokens:
        tvalue = token[0]
        ttype = token[1]
        #
        if ttype in type_all:
            para = 0
            impact = 0
            stem = stemmer.stem(tvalue) #理解为提取词根的方法（其实不一定提取到的是词根）
            if stem in vword:
                para = 1
                impact = vword[stem]
            else:
                freq = []
                syns = util.get_synonyms(stem)  #理解为获取stem的同义词
                for syn in syns:
                    score = 0
                    stem = util.get_stemmed(syn)
                    if stem in vword:
                        score = vword[stem]
                    freq.append(score)
                idx_max_freq = -1
                if len(freq) > 0:
                    idx_max_freq = freq.index(max(freq))
                if idx_max_freq > -1:
                    tvalue = syns[idx_max_freq]
                    para = 1
                    impact = vword[tvalue]
            if ttype in type_nn and stem in vjdk:
                para = 2
                impact = vjdk[stem]
            tvalue = util.get_stemmed(tvalue)

            vector = [tvalue, ttype, para, impact]
            data.append(vector)
    return data


def     parse(query):
    """
    这个函数执行内容为论文中的第二阶段中的步骤1：查询理解

    :param query:搜索内容
    :return: 一个列表，列表中的第一个元素为处理后的查询词列表，第二个元素为单词列表的importance
    """
    items = query_parse(query,
                        path_parsed_vocab='data/parsed_vocab_jdk_item.pkl',
                        path_method_vocab='data/method_vocab_stemed.pkl')

    # sorting words
    mid_list1 = list()  #重要性为1的连词等
    mid_list2 = list()
    word_list1 = list()
    word_list2 = list()
    other_list1 = list()
    other_list2 = list()
    for j in range(len(items)):
        item = items[j]
        #类型在type_cc type_to type_in中，为连词、介词等
        if item[1] in type_cc + type_to + type_in:
            if item[2] == 1:
                #list中只添加下标和对应的”重要性“
                mid_list1.append([j, items[j][3]])
            else:
                mid_list2.append([j, items[j][3]])
        #动词或名词
        elif item[1] in type_vb + type_nn:
            if item[2] == 1:
                word_list1.append([j, items[j][3]])
            else:
                word_list2.append([j, items[j][3]])
        # 其他词
        else:
            if item[2] == 1:
                other_list1.append([j, items[j][3]])
            else:
                other_list2.append([j, items[j][3]])

    #排序（应该是按照重要性）
    mid_list1.sort(key=operator.itemgetter(1))
    mid_list2.sort(key=operator.itemgetter(1))
    word_list1.sort(key=operator.itemgetter(1))
    word_list2.sort(key=operator.itemgetter(1))
    other_list1.sort(key=operator.itemgetter(1))
    other_list2.sort(key=operator.itemgetter(1))

    sort_list = mid_list1 + mid_list2 + other_list1 + other_list2 + word_list1 + word_list2
    #sort_list中存储的为单词在items中的下标，也是在query_list中的下标
    for j in range(len(sort_list)):
        sort_list[j] = sort_list[j][0]

    query_list = list()
    for item in items:
        query_list.append(item[0])

    line = [query_list, sort_list]
    return line
