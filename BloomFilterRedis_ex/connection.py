import redis


def bloom_filter_from_defaults(redis_url):
    _redis = redis.StrictRedis
    return _redis.from_url(redis_url)
