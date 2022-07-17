import redis
import json
import logging
import json
import functools

logging.basicConfig(format=u'[%(asctime)s] %(levelname).1s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO
                    )


def retry(max_tries):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for n in range(1, max_tries + 1):
                try:
                    return func(*args, **kwargs)
                except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
                    logging.info('connection lost %s times' % n)
                    if n == max_tries:
                        raise
        return wrapper
    return decorator


class Store(object):
    def __init__(self, host='localhost', port='6379', db=0, socket_timeout=5):
        self.host = str(host)
        self.port = int(port)
        self.db = int(db)
        self.socket_timeout = int(socket_timeout)
        self._r = redis.Redis(host=self.host, port=self.port, db=self.db, socket_timeout=self.socket_timeout)


    @retry(1)
    def cache_get(self, key):
        val = self._r.get(key)
        logging.info("key %s get from cache" % key)
        return json.loads(val.decode("utf-8")) if val else None


    @retry(4)
    def cache_set(self, key, value, ttl):
        value = json.dumps(value)
        logging.info("key %s stored in cache" % key)
        self._r.set(key, value, ttl)
        return

    @retry(4)
    def get(self, key):
        value = self.cache_get(key)
        if value is None:
            raise RuntimeError("Key %s is not set!" % key)
        return value

