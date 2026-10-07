from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

USER_SERVICE = os.getenv(
    "USER_SERVICE",
    "http://localhost:5001"
)

FOOD_SERVICE = os.getenv(
    "FOOD_SERVICE",
    "http://localhost:5002"
)


@app.route('/')
def home():
    return "Order Service is running"


@app.route('/order/<int:user_id>/<int:food_id>')
def create_order(user_id, food_id):

    user_response = requests.get(
        f"{USER_SERVICE}/user/{user_id}"
    )

    food_response = requests.get(
        f"{FOOD_SERVICE}/food/{food_id}"
    )

    user = user_response.json()
    food = food_response.json()

    return jsonify({
        "message": "Order created successfully",
        "user": user,
        "food": food
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)