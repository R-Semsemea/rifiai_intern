from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/students')
def getData():
    data = [
        {"name": "Sara Ahmad", "age": 21, "specialization": "Computer Science"},
        {"name": "Omar Khaled", "age": 22, "specialization": "Information Technology"},
        {"name": "Lina Nasser", "age": 20, "specialization": "Software Engineering"},
        {"name": "Kareem Youssef", "age": 23, "specialization": "Cybersecurity"},
        {"name": "Maya Hatem", "age": 22, "specialization": "AI & Machine Learning"},
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)