from flask import Flask, request, jsonify

app = Flask(__name__)

# Talabalar ro'yxati
students = []

# Talabani ro'yxatdan o'tkazish
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    students.append(data)
    return jsonify({"message": "Ro'yxatdan o'tkazildi"}), 201

# Ro'yxatni olish
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

if __name__ == '__main__':
    app.run(debug=True)
