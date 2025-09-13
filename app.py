from flask import Flask, request, jsonify, send_from_directory
from SpaceGen.model import SpaceGenModel
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
MODEL_PATH = "SpaceGen/SpaceGen_Large.keras"



model = SpaceGenModel(model_path=MODEL_PATH)
@app.route('/api/data', methods=['POST'])
def space_text():
    if request.is_json:
        data = request.get_json()
        corrupted_text = data.get('corrupted_text')
        spaced_text = model.fix_space(corrupted_text)
        return jsonify({'spaced_text': spaced_text})

@app.get('/')
def index():
    return send_from_directory('.', 'main.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)