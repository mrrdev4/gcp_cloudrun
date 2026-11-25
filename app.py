import os

from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/")
def hello() -> Response:
    return jsonify(
        {
            "status": "ok",
            "message": "Hello World from Cloud Run!",
            "app_env": os.environ.get("APP_ENV", "local"),
            "log_level": os.environ.get("LOG_LEVEL", "INFO"),
            "timezone": os.environ.get("TZ", "UTC"),
            "service": os.environ.get("K_SERVICE", "local"),
            "revision": os.environ.get("K_REVISION", "local"),
        }
    )


@app.route("/health")
@app.route("/healthz")
def health() -> tuple[Response, int]:
    return (
        jsonify(
            {
                "status": "healthy",
                "env": os.environ.get("APP_ENV", "local"),
            }
        ),
        200,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="127.0.0.1", port=port)
