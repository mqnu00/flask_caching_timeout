from flask import Flask
from cache import Cache

app = Flask(__name__)
cache = Cache(app=app)


@app.route('/<int:ttt>')
@cache.cached
def hello_world(ttt):  # put application's code here
    return f'{ttt}'


if __name__ == '__main__':
    app.run()
