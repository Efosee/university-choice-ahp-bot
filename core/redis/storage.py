from aiogram.fsm.storage.redis import RedisStorage

storage = RedisStorage.from_url('redis://localhost:6379/0')
#from aiogram.fsm.storage.memory import MemoryStorage
#storage2 = MemoryStorage()
"""
Есть 2 варианта инциализации редиса:

1) Установить пакет aioredis, создать redis = Redis() по умолчанию локальный хост
Далее создать storage = RedisStorage(redis=redis) передать в парметр redis экземлпяр класса redis:
from aioredis import Redis
redis = Redis()
storage = RedisStorage(redis=redis)

2) Воспользоваться методом у класса storage = RedisStorage.from_url(url=url)
По умолчанию url = 'redis://localhost:6379/0'
"""