from flask import Flask
from cache import Cache

app = Flask(__name__)
cache = Cache(app=app, config={
    'CACHE_TYPE': 'simple',
    'REFRESH_TYPE': 'LFU',
    'ENABLE_TTL': True,
    'CACHE_THRESHOLD': 5,
    'CACHE_DEFAULT_TIMEOUT': 3
})


@app.route('/<int:ttt>')
@cache.cached
def hello_world(ttt):  # put application's code here
    return f'{ttt}'


if __name__ == '__main__':
    app.run()
