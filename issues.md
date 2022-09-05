### 1. Elasticsearch Error: ERROR Unable to invoke factory method in class org.apache.logging.log4j.core.appender.RollingFileAppender for element RollingFile...

```
chown -R user ./logs/
chgrp -R user ./logs/
```

### 2. Flask Warning: Use a production WSGI server instead

```
from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0',5000),app)
    server.serve_forever()
```
