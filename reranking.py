import util
import operator
import re


def matcher_name(words, line, cmd):
    """
    用论文中的方程1计算Sname

    :param words: 查询词列表
    :param line: 查询结果中的方法
    :param cmd: es查询用的正则表达式
    :return:Sname的值
    """
    cmd = str(cmd).replace('.*', ' ').strip().split(' ')
    line = str(line).replace('\n', '')

    word_usage = len(cmd) / len(words)
    line_coverage = len(''.join(cmd)) / len(line)
    score = word_usage * line_coverage
    return score


def matcher_api(query, line, jdk):
    """

    :param query:查询词列表
    :param line: 返回结果中"paesed对应的内容"
    :param jdk: jdk文件反序列化的对象
    :return:
    """
    line = str(line).replace('\n', '').lower()
    index = []
    freq = 0
    count = 0
    for word in query:
        pattern = re.compile(word.lower())
        wi = [i.start() for i in pattern.finditer(line)]
        if len(wi) > 0:
            freq += len(wi) * len(word)
            count += 1
            index.append(wi)
    word_usage = count / len(query)
    line_coverage = freq / len(line)
    max_sequence = len(sequence(index)) / len(query)

    apis = line.split(',')
    api_count = 0
    jdk_count = 0
    for api in apis:
        if '.' in api:
            api_count += 1
            if '(' in api or '[' in api or '<' in api:
                api = api[:api.rfind('.')]
            if api in jdk:
                jdk_count += 1
    jdk_percent = 0
    if api_count > 0:
        jdk_percent = jdk_count / api_count

    score = word_usage * line_coverage * max_sequence * jdk_percent
    return score


def sequence(seq):
    orders = []
    scores = []
    for i in range(len(seq)):
        scores.append(0)
        for si in seq[i]:
            orders.append([si])
        for k in range(len(orders)):
            sik = orders[k][-1]

            for j in range(i + 1, len(seq)):
                for l in range(len(seq[j])):
                    sjl = seq[j][l]

                    if sik < sjl:
                        temp = []
                        temp.extend(orders[k])
                        temp.append(sjl)
                        orders.append(temp)
    for o in orders:
        scores[len(o) - 1] += 1
    return scores


def reranking(query_parse, data, cmds, jdk):
    """

    :param query_parse: 一个列表，列表中的第一个元素为处理后的查询词列表，第二个元素为单词列表的importance
    :param data: 模糊查询结果列表
    :param cmds: 模糊查询结果列表对应的查询正则表达式
    :return:展示给用户的结果
    """
    # jdk = util.load_pkl('data/jdk_vocab.pkl')
    query = query_parse[0]

    lines = []

    scores = list()
    for j in range(len(data)):
        res = data[j]['_source']
        line = res['method']
        cmd = cmds[j]
        scores.append([j, matcher_name(query, line, cmd)])
    scores.sort(key=operator.itemgetter(1), reverse=True)

    scores = scores[:100]
    for j in range(len(scores)):
        idx = scores[j][0]
        res = data[idx]['_source']
        line = res['parsed']
        scores[j].append(matcher_api(query, line, jdk))
    scores.sort(key=operator.itemgetter(1, 2), reverse=True)

    count = 10
    if len(data) < 10:
        count = len(data)
    for j in range(count):
        idx = scores[j][0]
        line = str(data[idx]['_source']['source'])

        token = 'for (int'
        if line.find(token) > -1:
            l = ''
            ds = line.split('for (int')
            l += ds[0]
            for k in range(1, len(ds)):
                db = str(ds[k])
                di = db.find('{')
                d = db[:di - 1]
                key = d[:d.find('=') - 1].strip()
                dd = d.split(key)
                keyy = '@ ' + key
                kk = ''
                for m in range(1, len(dd) - 1):
                    if dd[m-1][-1].isalnum() and dd[m][0].isalnum():
                        kk += key + dd[m]
                    else:
                        kk += keyy + dd[m]
                kk += dd[-1]

                # dd = dd[0] + keyy.join(dd[1:])
                l += token + ' ' + key + kk + db[di:]
            line = l
            print()

        lines.append(line)

    return lines
