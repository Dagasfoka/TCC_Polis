# backend/app/scripts/test_redis.py

from backend.app.db.redis import redis_client


def test():
    redis_client.set("teste", "funcionando")
    value = redis_client.get("teste")
    print(value)

if __name__ == "__main__":
    test()