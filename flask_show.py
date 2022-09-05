from flask import Flask, render_template, jsonify, request
import util
import parsing
from indexing import SearchEngine
import reranking

se = SearchEngine()
app = Flask(__name__)
jdk = util.load_pkl('data/jdk_vocab.pkl')


@app.route('/')
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print('ip:', ip)
    return render_template('index.html')


@app.route('/search/<query>', methods=['POST', 'GET'])
def search(query):
    print(query)
    query_parse = parsing.parse(query)
    print(1)
    data, cmds = se.fuzzy_search(query_parse, top_k=10)
    results = reranking.reranking(query_parse, data, cmds, jdk)
    print(3)
    # print(results)
    # return render_template('search.html',results=results)
    json = jsonify({"result": results})
    return json


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
