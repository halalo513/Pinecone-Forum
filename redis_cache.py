from redis import Redis

# 配置Redis, 有密码就配置密码，没有密码就删掉password字段
cache = Redis(host='127.0.0.1', port=6379, password='')