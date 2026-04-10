from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
import os
from flask_migrate import Migrate

redis_client = None
task_queue = None


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@postgres:5432'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_client = Redis.from_url(redis_url)
task_queue = Queue(connection=redis_client)

with app.app_context():
    db.create_all()
