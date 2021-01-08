from huey import RedisExpireHuey
from redis import ConnectionPool


pool = ConnectionPool(
    host='127.0.0.1',
    port=6379,
    max_connections=20,
)
HUEY = RedisExpireHuey(
    name='ci_ynh',  # Just the name for this task queue.
    connection_pool=pool,  # Use a connection pool to redis.
    results=True,  # Store return values of tasks.
    store_none=False,  # If a task returns None, do not save to results.
    utc=True,  # Use UTC for all times internally.
    expire_time=24 * 60 * 60,  # cleaned-up unread task results from Redis after 24h
)
