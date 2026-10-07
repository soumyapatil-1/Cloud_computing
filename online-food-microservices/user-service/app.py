from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "User Service is running"


@app.route('/user/<int:user_id>')
def get_user(user_id):
    return jsonify({
        "user_id": user_id,
        "name": "Soumya",
        "status": "Active"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)