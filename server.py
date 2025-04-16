from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/update', methods=['POST'])
def update_data():
    content = request.json
    with open('data.json', 'w') as f:
        json.dump(content, f)
    return jsonify({"message": "Data updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
