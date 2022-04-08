from flask import Flask, request, jsonify
import requests
from flask_caching import Cache
from functools import wraps
import datetime

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
cache = Cache(app)

def time(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        s = datetime.datetime.now()
        _ = function(*args, **kwargs)
        e = datetime.datetime.now()
        app.logger.info("Execution Time : {} ".format(e-s))
        return _
    return wrapper

@app.route("/universities")
@time
@cache.cached(timeout=30, query_string=True)
def get_universities():
    API_URL = "http://universities.hipolabs.com/search?country="
    search = request.args.get('country')
    r = requests.get(f"{API_URL}{search}")
    return jsonify(r.json())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)