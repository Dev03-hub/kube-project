from flask import Flask, jsonify, request

app = Flask(__name__)

users = [{"id": 1, "name": "Debraj"}]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    users.append({"id": len(users)+1, "name": data['name']})
    return jsonify({"message": "User added"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)