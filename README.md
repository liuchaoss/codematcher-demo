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
1. install Elasticsearch 8.2

`https://www.elastic.co/downloads/past-releases#elasticsearch`

2. start Elasticsearch

`./elasticsearch-8.2.0/bin/elasticsearch`

3. download data to ./unzipdata/ 

```
Link: https://pan.baidu.com/s/13Ge4EhUjyN-XTtA2mUBlLg
Access key: txs6
```

4. fill data into Elasticsearch and build indexing

`python indexing.py`

5. start flask

`python flask_show.py`
