from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "Food Service is running"


@app.route('/food/<int:food_id>')
def get_food(food_id):
    return jsonify({
        "food_id": food_id,
        "food": "Pizza",
        "price": 250
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)