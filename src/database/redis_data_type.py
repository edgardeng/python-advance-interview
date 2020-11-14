"""
Redis Test Demo 测试案例


"""
import json
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

def string_cache():
    data = {'a': 1, 'b': 2}
    redis.set('cache-key', json.dumps(data))
    print(' set cache-key with value:', data)
    result = json.loads(redis.get('cache-key'))
    print(' get cache-key with value:', result)

def list_queue():
    print(' push data to queue')
    # https://segmentfault.com/a/1190000008404117

if __name__ == '__main__':
    string_cache()
