import os

class Config:
    SECRET_KEY            = os.getenv('SECRET_KEY', 'devkey')
    FEEDS_FILE            = 'feeds.json'
    CACHE_TYPE            = 'simple' 
    CACHE_DEFAULT_TIMEOUT = 600 
