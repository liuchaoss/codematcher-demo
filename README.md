### ***introduction***
This is a tool demo for our prior work CodeMatcher

```
@article{liu2021codematcher,
  title={CodeMatcher: Searching Code Based on Sequential Semantics of Important Query Words},
  author={Liu, Chao and Xia, Xin and Lo, David and Liu, Zhiwe and Hassan, Ahmed E and Li, Shanping},
  journal={ACM Transactions on Software Engineering and Methodology (TOSEM)},
  volume={31},
  number={1},
  pages={1--37},
  year={2021},
  publisher={ACM New York, NY}
}
```

### ***working with CodeMatcher***
***1. install and start Elasticsearch 8.2***

- download

`https://www.elastic.co/downloads/past-releases#elasticsearch`

- start

`./elasticsearch-8.2.0/bin/elasticsearch`

- check status

`http://x.x.x.x:9200`

***2. get source code***

- clone source code

`git clone https://github.com/liuchaoss/codematcher-demo.git`

- install dependencies

`pip install -r requirements.txt`

***3. download and fill data***

- download data to ./unzipdata/ 

```
Link: https://pan.baidu.com/s/13Ge4EhUjyN-XTtA2mUBlLg
Access key: txs6

Google Drive: https://drive.google.com/drive/folders/1c5GHMlBfclr6U27vn5Vy10V8RiHBcASs
```

- fill data into Elasticsearch and build indexing

`python indexing.py`

***4. start code search engine***

- start flask

`python flask_show.py`

- check the status of codematcher

`http://x.x.x.x:5000`
