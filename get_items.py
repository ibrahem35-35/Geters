from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/get_items', methods=['POST'])
def get_items():
    try:
        data = request.get_json()
        if data and 'data' in data and 'items' in data['data']:
            items_list = data['data']['items']
            return jsonify(items_list)
        else:
            error_message = {"error": "Data format is incorrect. Missing 'data' or 'items'."}
            return jsonify(error_message), 400
    except Exception as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'
    app.run(debug=False, host=host, port=port)
