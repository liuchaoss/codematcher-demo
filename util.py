import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re
import pickle as pk
import csv

# number, adjective, noun, adverb, verb,
type = ['CD',
        'JJ', 'JJR', 'JJS',
        'NN', 'NNS', 'NNP', 'NNPS',
        'RB', 'RBR', 'RBS',
        'VB', 'VBD', 'VBG', 'VBN', 'VNP', 'VBZ']


def curl_cmd(url, path):
    return 'curl ' + url + ' -o ' + path


def load_txt(path):
    with open(path, 'r', encoding='utf-8') as infile:
        return infile.readlines()


def save_txt(path, lines):
    with open(path, 'w', encoding='utf-8') as infile:
        infile.writelines(lines)


def load_csv(path):
    with open(path, 'r', encoding='utf-8') as file_reader:
        csv_reader = csv.reader(file_reader, delimiter=',')
        lines = []
        for line in csv_reader:
            lines.append(line)
        return lines


def save_csv(path, lines, de):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=de)
        writer.writerows(lines)


def save_pkl(path, data):
    pk.dump(data, open(path, 'wb'))


def load_pkl(path):
    return pk.load(open(path, 'rb'))


def camel_split(name):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower().replace('_', ' ')


def camel_split_for_tokens(name):
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower().replace('_', ' ')
    name = re.findall(r'[0-9]+|[a-z]+', name)
    return name


def get_camels(lines):
    data = list()
    for line in lines:
        if len(line) == 0:
            data.append([])
            continue
        data.append(camel_split(line))
    return data


def filter_digit_english(line):
    return re.sub(r'[^\x30-\x39, ^\x41-\x5A,^\x61-\x7A]+', ' ', line)


def get_filters(lines):
    data = list()
    for line in lines:
        if len(line) == 0:
            data.append([])
            continue
        data.append(filter_digit_english(line))
    return data


def remove_stopwords(tokens):
    clean_tokens = list()
    sr = stopwords.words('english')
    for token in tokens:
        if token not in sr:
            clean_tokens.append(token)
    return clean_tokens


def remove_keywords(tokens):
    clean_tokens = list()
    sr = dict(load_pkl('data/keywords_vocab.pkl')).keys()
    for token in tokens:
        if token not in sr:
            clean_tokens.append(token)
    return clean_tokens


def get_synonyms(token):
    synonyms = []
    for syn in wordnet.synsets(token):
        for lemma in syn.lemmas():
            lem = lemma.name()
            if lem not in synonyms and lem != token:
                synonyms.append(lem)
    return synonyms


def get_stemmed_words(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = list()
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
    return stemmed_tokens


def get_stemmed(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def get_stemmed_lines(lines):
    data = list()
    for line in lines:
        if len(line) == 0:
            data.append([])
            continue
        data.append(get_stemmed_words(line))
    return data


def get_tokens(line):
    tokens = list()
    for token in word_tokenize(line, 'english'):
        if len(token) > 1:
            if '-' in token:
                ts = token.split('-')
                for t in ts:
                    tokens.append(t)
            else:
                tokens.append(token)
    return tokens


def get_tokens_lines(lines):
    data = list()
    for line in lines:
        if len(line) == 0:
            data.append([])
            continue
        data.append(get_tokens(line))
    return data


def get_jdk_objects(tokens):
    jdk = dict(load_pkl('data/jdk_vocab.pkl'))
    objects = list()
    for token in tokens:
        if token in jdk.values():
            key = list(jdk.keys())[list(jdk.values()).index(token)]
            objects.append(key)
    return objects


def get_token_class(tokens):
    used_tokens = list()
    tokens = nltk.pos_tag(tokens)
    for token in tokens:
        if token[1] in type:
            used_tokens.append(token[0])
    return used_tokens


def filter_tokens(tokens):
    filterred_tokens = list()
    for token in tokens:
        token = re.sub('[^a-zA-Z0-9 ]', ' ', token)
        token = re.sub(' +', ' ', token).strip()
        if ' ' in token:
            filterred_tokens.extend(token.split(' '))
        else:
            filterred_tokens.append(token)
    return filterred_tokens


def match(key, line):
    return [i.start() for i in re.compile(key).finditer(line)]


def data2txt(path_from, path_to):
    lines = load_pkl(path_from)
    with open(path_to, 'w', encoding='utf-8') as f:
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                ls = lines[i][j]
                for k in range(len(ls)):
                    f.write(str(ls[k]))
                    if k < len(ls) - 1:
                        f.write(',')
                if j < len(lines[i]) - 1:
                    f.write(';')
            if i < len(lines) - 1:
                f.write('\n')


def txt2data(path_from):
    lines = load_txt(path_from)
    data = []
    for line in lines:
        ls = line.split(';')
        data_row = []
        for i in range(len(ls)):
            l = ls[i].split(',')
            for j in range(2, len(l)):
                l[j] = int(l[j])
            data_row.append(l)
        data.append(data_row)
    return data


if __name__ == '__main__':
    # data2txt('data/queries_parse.pkl', 'data/queries_parse.txt')
    data = txt2data('data/queries_parse.txt')
    print()
    # a = get_synonyms('concatenation')
    # a = camel_split_for_tokens('convertA22B')
    # print(a)
    # b = nltk.pos_tag(a)
    # print(b)
    # nltk.download()
    # print(get_synonyms('square'))
    # print(camel_split('CasdfSaaDkkd'))
    # jacoma_query()
    # jacoma_code()
    # lem = WordNetLemmatizer()
    # print(lem.lemmatize('ini', 'v'))
    # save_csv('f://test.txt', [[1, 2, 3], [4, 5, 6]])