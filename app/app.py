from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Debraj"}
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "user-service",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json(silent=True)

    if not data or not data.get("name"):
        return jsonify({
            "error": "name is required"
        }), 400

    user = {
        "id": len(users) + 1,
        "name": data["name"]
    }

    users.append(user)

    return jsonify({
        "message": "User added",
        "user": user
    }), 201


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
