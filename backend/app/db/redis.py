import redis
from backend.app.core.config import settings

#redis_client = redis.Redis(
#    host=settings.REDIS_HOST,
#   port=settings.REDIS_PORT,
#    db=0,
#    decode_responses=True
#)
import os


redis_client = redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True
)
