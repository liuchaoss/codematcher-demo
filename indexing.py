from elasticsearch import Elasticsearch
from elasticsearch import helpers
import hashlib
import util
import os
import re

jdk = util.load_pkl('data/jdk_vocab.pkl')


class SearchEngine:
    def __init__(self):
        self.index = "search_engine"
        self.ip = "http://localhost:9200"
        self.es = Elasticsearch(self.ip).options(ignore_status=400)
        self.indices = self.es.indices

    def create_index(self):
        mappings = {
            "properties": {
                "method": {"type": "text"},
                "parsed": {"type": "text"},
                "source": {"type": "text"}
            }
        }
        # print(self.indices.create(index=self.index, mappings=mappings))
        settings = {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "my_tokenizer"
                    }
                },
                "tokenizer": {
                    "my_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 3,
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                }
            }
        }
        print(self.indices.create(index=self.index, mappings=mappings, settings=settings))

    def remove_index(self):
        print(self.indices.delete(index=self.index))

    def put_mapping(self):
        print(self.indices.put_mapping(index=self.index))

    def put_setting(self):
        print(self.indices.put_settings(index=self.index))

    def fill_data(self, path):
        for i in range(166):
            print(i)
            body = util.load_pkl(path + 'data' + str(i) + '.pkl')
            helpers.bulk(self.es, body, )

    def transform_data(self, path):
        idx = 0
        for i in range(10):
            for j in range(20):
                print(i, j)
                file = path + 'body' + str(i) + '-' + str(j) + '.pkl'
                if os.path.exists(file):
                    body = util.load_pkl(file)
                    for k in range(len(body)):
                        del body[k]['_source']['comment']
                        del body[k]['_source']['javadoc']
                        del body[k]['_source']['modifier']
                        del body[k]['_source']['package']
                        del body[k]['_source']['parameter']
                        del body[k]['_source']['return']
                    print()
                    util.save_pkl(path + 'data' + str(idx) + '.pkl', body)
                    idx += 1
                else:
                    break

    def filter_data(self, path):
        hash_set = set()

        for i in range(166):
            body = []
            data = util.load_pkl(path + 'data' + str(i) + '.pkl')
            for j in range(len(data)):
                source = data[j]['_source']['source']
                hash_val = hashlib.md5(source.encode('utf-8')).digest()
                if not hash_set.__contains__(hash_val):
                    hash_set.add(hash_val)
                    body.append(data[j])
                print()
            util.save_pkl(path + 'body' + str(i) + '.pkl', body)
            print()

    def clean_data(self, path):
        for i in range(166):
            body = []
            data = util.load_pkl(path + 'body' + str(i) + '.pkl')
            for j in range(len(data)):
                method = data[j]['_source']['method']
                flag = 0
                for k in method:
                    if ord(k) > 127:
                        flag = 1
                        break
                if flag == 0:
                    body.append(data[j])
            util.save_pkl(path + 'data' + str(i) + '.pkl', body)

    def fuzzy_search(self, query_parse, top_k):
        """
        调用elasticsearch搜索引擎去搜索top_k个查询词

        :param query_parse: 解析后的查询词，具体来说，列表的第一个元素是处理后的查询词列表，第二个元素是排序后的下标，下标指示其在第一个元素中的位置
        :param top_k: 要求返回多少条结果
        :return: 一个元组，第一个元素是elasticsearch返回的结果列表，第二个元素是查询内容列表，两者一一对应
        """
        query = query_parse
        query_words = list(query[0])
        query_sorts = list(query[1])

        # .表示匹配除换行符\n之外的任何单字符，*表示零次或多次。
        cmd = '.*' + '.*'.join(query_words) + '.*'
        data = []
        cmds = []
        source_hash = []
        respond, query_cmd = self.search_respond(cmd, source_hash)
        data.extend(respond)
        cmds.extend(query_cmd)
        idx = 0
        while len(data) < top_k and len(query_words) - idx >= 2:
            temp = []
            if idx == 0:
                s = [query_sorts[0]]
            else:
                s = query_sorts[:idx]
            for j in range(len(query_words)):
                if j not in s:
                    temp.append(query_words[j])
            cmd = '.*'.join(temp) + '.*'
            respond, query_cmd = self.search_respond(cmd, source_hash)
            data.extend(respond)
            cmds.extend(query_cmd)
            idx += 1

        n_data = len(data)
        if n_data < 10:
            query = ' '.join(query_words)
            respond, query_cmd = self.search_respond_more(cmd, source_hash, n_data, query)
            data.extend(respond)
            cmds.extend(query_cmd)

        return data, cmds

    def search_test(self):
        cmd = "*.for.*"
        query = {
            # "sort": [{"_score"}],
            "query": {"regexp": {"source": cmd}}
        }
        scan_resp = helpers.scan(self.es, query, index=self.index, scroll="10m")
        respond = []
        i = 0
        for hit in scan_resp:
            i = i + 1
            respond.append(hit)
            print(i)
        print()

    def search_respond_more(self, cmd, source_hash, n_data, query):
        query = {"query": {"match": {"source": query.lower()}}}
        scan_resp = helpers.scan(self.es, query, index=self.index, scroll="10m")
        respond = []
        query_cmd = []
        for hit in scan_resp:
            source = str(hit['_source']['source'])
            hash_val = hashlib.md5(source.encode('utf-8')).digest()
            if hash_val not in source_hash:
                source_hash.append(hash_val)
                respond.append(hit)
                query_cmd.append(cmd)
                n_data += 1
                if n_data == 10:
                    break
        return respond, query_cmd

    def search_respond(self, cmd, source_hash):
        """
        用cmd执行elasticsearch，去重后返回源代码

        :param cmd: 正则匹配串
        :param source_hash:保存搜索到代码串的hash值列表
        :return:{respond}是去重后的源代码列表，{query_cmd}是查询的正则串列表，两者一一对应
        """
        n_words = len(cmd.split('.*'))
        if n_words <= 3:
            cmd = re.sub('\.\*', '', cmd)
            query = {"query": {"match": {"source": cmd.lower()}}}
        else:
            query = {"query": {"regexp": {"method": cmd.lower()}}}
        scan_resp = helpers.scan(self.es, query, index=self.index, scroll="10m")
        respond = []
        query_cmd = []
        idx = 0
        for hit in scan_resp:
            source = str(hit['_source']['source'])
            hash_val = hashlib.md5(source.encode('utf-8')).digest()
            if hash_val not in source_hash:
                source_hash.append(hash_val)
                respond.append(hit)
                query_cmd.append(cmd)
                idx += 1
                if n_words <= 3 and idx == 1000:
                    break
        return respond, query_cmd

    def search(self):
        query = 'get123'
        import parsing
        query_parse = parsing.parse(query)
        print(1)
        data, cmds = self.fuzzy_search(query_parse, top_k=10)
        import reranking
        results = reranking.reranking(query_parse, data, cmds, jdk)
        print(3)
        print(results)


if __name__ == '__main__':
    se = SearchEngine()
    se.create_index()
    se.fill_data('unzipdata')
