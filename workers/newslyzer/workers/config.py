from os import environ

redis_host = environ.get('REDIS_HOST', 'localhost')
redis_port = environ.get('REDIS_PORT', '6379')
redis_connection = 'redis://{}:{}'.format(redis_host, redis_port)

word_cloud_path = environ.get('WORDCLOUD_PATH', '/tmp/wordcloud')
