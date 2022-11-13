from flask import Flask, render_template, jsonify, request
import util
import parsing
from indexing import SearchEngine
import reranking
import logging
from flask_cors import CORS

se = SearchEngine()
app = Flask(__name__)
jdk = util.load_pkl('data/jdk_vocab.pkl')
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    app.logger.info(f"access from ip:{ip}")
    return render_template('index.html')


@app.route('/search/<query>', methods=['POST', 'GET'])
def search(query):
    app.logger.info("query" + "*" * 50)
    app.logger.info(query)
    query_parse = parsing.parse(query)

    data, cmds = se.fuzzy_search(query_parse, top_k=10)
    results = reranking.reranking(query_parse, data, cmds, jdk)
    app.logger.info("results" + "*" * 50)
    for result in results:
        app.logger.info(result)

    json = jsonify({"result": results})
    return json


def logging_setting():
    handler1 = logging.FileHandler(filename="flask.log", encoding="utf-8")
    # handler2 = logging.StreamHandler()

    app.logger.setLevel(logging.DEBUG)
    handler1.setLevel(logging.INFO)
    # handler2.setLevel(logging.NOTSET)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
    handler1.setFormatter(formatter)
    # handler2.setFormatter(formatter)

    app.logger.addHandler(handler1)
    # app.logger.addHandler(handler2)


if __name__ == '__main__':
    # setting debug as True if you want to see details
    # app.debug = True
    logging_setting()
    app.run(host='0.0.0.0')

