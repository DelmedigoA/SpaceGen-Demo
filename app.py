from flask import Flask, request, jsonify, send_from_directory
from SpaceGen.model import SpaceGenModel
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

model = SpaceGenModel()

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

if __name__ == '__main__':
    # Use a non-conflicting port to avoid macOS AirPlay/other listeners
    app.run(debug=True)
