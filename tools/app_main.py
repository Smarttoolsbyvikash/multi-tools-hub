from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder=None)

# ------------------------
# 🔹 Base directories setup
# ------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
UPLOADS_DIR = os.path.join(PARENT_DIR, 'uploads')

# Ensure folders exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

# ------------------------
# 🔹 Home route
# ------------------------
@app.route('/')
def home():
    return send_from_directory(PARENT_DIR, 'index.html')

# ------------------------
# 🔹 Universal HTML route (auto serve any .html file)
# ------------------------
@app.route('/<path:filename>')
def serve_any_html(filename):
    """
    Automatically serves any HTML file inside main folder or 'tools' folder.
    Example: /qr-generator.html or /audio-cutter.html
    """
    # Main level file (like age-calculator.html)
    main_path = os.path.join(PARENT_DIR, filename)
    tools_path = os.path.join(BASE_DIR, filename)
    uploads_path = os.path.join(UPLOADS_DIR, filename)

    # Serve file from available location
    if os.path.exists(main_path):
        return send_from_directory(PARENT_DIR, filename)
    elif os.path.exists(tools_path):
        return send_from_directory(BASE_DIR, filename)
    elif os.path.exists(uploads_path):
        return send_from_directory(UPLOADS_DIR, filename)
    else:
        return "404 - File Not Found", 404


# ------------------------
# 🔹 Run server
# ------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
