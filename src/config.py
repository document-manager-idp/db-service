import os

class Config:
    SECRET_KEY = os.environ.get('OPENSEARCH_INITIAL_ADMIN_PASSWORD')
    DEBUG = True
    CORS_HEADERS = 'Content-Type'
