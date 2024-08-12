# wsgi.py

from app.main import app
from fastapi.middleware.wsgi import WSGIMiddleware

application = WSGIMiddleware(app)
