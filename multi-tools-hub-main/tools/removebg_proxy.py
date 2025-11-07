from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)  # Allow frontend (HTML) to call backend

# 👉 Apni API key daalna yahan (remove.bg ka key)
API_KEY = "hc8KkaoFRySjqaPutTKwWqkv"

@app.route('/')
def home():
    return jsonify({"status": "Background Remover API running ✅"})

@app.route('/removebg', methods=['POST'])
def remove_bg():
    try:
        if 'image_file' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files['image_file']
        image_data = file.read()

        # remove.bg API endpoint
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': ('image.png', image_data)},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code == 200:
            return send_file(BytesIO(response.content), mimetype='image/png')
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 Render ke liye fix (automatic PORT binding)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
