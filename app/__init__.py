import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue

db = SQLAlchemy()
migrate = Migrate()
redis_client = None
task_queue = None
app = Flask(__name__)


def _configure_app() -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    global redis_client, task_queue
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_client = Redis.from_url(redis_url)
    task_queue = Queue(connection=redis_client)


_configure_app()

with app.app_context():
    from app.models import Category, Task


@app.get("/")
def index():
    return {
        "message": "Task Manager API is running",
        "endpoints": ["/tasks", "/categories", "/health"],
    }, 200


@app.get("/health")
def health():
    return {"status": "ok"}, 200



from app.routes import categories, tasks  


def create_app() -> Flask:
    return app
