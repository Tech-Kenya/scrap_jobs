from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from flask_caching import Cache
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='../dist', static_url_path='/')
CORS(app)

# Enhanced cache configuration
cache = Cache(
    config={
        "CACHE_TYPE": "SimpleCache",  # Use 'RedisCache' or 'MemcachedCache' in production
        "CACHE_DEFAULT_TIMEOUT": 86400,  # 24 hours in seconds
        "CACHE_THRESHOLD": 1000,  # Maximum number of items to cache
        "CACHE_IGNORE_ERRORS": True,  # Continue if caching fails
    }
)
cache.init_app(app)

JOBS_FILE = "services/jobs.json"
REPOS_FILE = "services/repos.json"
CACHE_TIMEOUT = 86400  # 24 hours in seconds

@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def generate_cache_key(endpoint, file_path):
    """Generate a consistent cache key based on endpoint and file modification time"""
    file_mtime = str(os.path.getmtime(file_path)) if os.path.exists(file_path) else "0"
    return f"{endpoint}_{file_mtime}"


def create_json_response(data, status=200):
    """Helper to create consistent JSON responses with caching headers"""
    response = make_response(jsonify(data) if isinstance(data, dict) else data)
    response.headers["Content-Type"] = "application/json"
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TIMEOUT}"
    response.headers["Expires"] = (
        datetime.utcnow() + timedelta(seconds=CACHE_TIMEOUT)
    ).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    cache_key = generate_cache_key("jobs", JOBS_FILE)

    # Try to get from cache first
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    # Cache miss - load from file
    if not os.path.exists(JOBS_FILE):
        return create_json_response({"error": "Jobs file not found"}, 404)

    try:
        with open(JOBS_FILE, "r", encoding="utf-8") as file:
            jobs_data = file.read()
            response = create_json_response(jobs_data)
            cache.set(cache_key, response, timeout=CACHE_TIMEOUT)
            return response
    except Exception as e:
        return create_json_response({"error": str(e)}, 500)


@app.route("/api/trending-repos", methods=["GET"])
def get_trending_repos():
    cache_key = generate_cache_key("repos", REPOS_FILE)

    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    if not os.path.exists(REPOS_FILE):
        return create_json_response({"error": "Repos file not found"}, 404)

    try:
        with open(REPOS_FILE, "r", encoding="utf-8") as file:
            repos_data = json.load(file)
            response = create_json_response(repos_data)
            cache.set(cache_key, response, timeout=CACHE_TIMEOUT)
            return response
    except Exception as e:
        return create_json_response({"error": str(e)}, 500)


@app.route("/api/cache-info", methods=["GET"])
def cache_info():
    """Endpoint to check cache status"""
    return jsonify(
        {
            "cache_type": app.config.get("CACHE_TYPE"),
            "cache_timeout": CACHE_TIMEOUT,
            "current_time": datetime.utcnow().isoformat(),
            "status": "Cache is working properly",
        }
    )


@app.route("/api/clear-cache", methods=["POST"])
def clear_cache():
    """Endpoint to manually clear cache (for debugging)"""
    try:
        cache.clear()
        return jsonify({"status": "Cache cleared successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
