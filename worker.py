import os

from redis import Redis
from rq import Connection, Worker


def main():
	redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
	redis_conn = Redis.from_url(redis_url)

	with Connection(redis_conn):
		worker = Worker(["default"])
		worker.work()


if __name__ == "__main__":
	main()
