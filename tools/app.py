from flask import Flask, render_template_string, request, send_file
import os
import imageio_ffmpeg as ffmpeg
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎵 Audio Trim Cutter</title>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #181818, #303030);
      color: white;
      text-align: center;
      padding: 40px;
    }
    h1 { color: #ffcc00; }
    .box {
      background: #222;
      padding: 25px;
      border-radius: 15px;
      width: 90%;
      max-width: 500px;
      margin: auto;
      box-shadow: 0 0 15px rgba(255,255,255,0.1);
    }
    input, button {
      margin: 8px;
      padding: 10px;
      border-radius: 10px;
      border: none;
      outline: none;
    }
    button {
      background: #ffcc00;
      font-weight: bold;
      cursor: pointer;
    }
    button:hover { background: #ffaa00; }
    audio { width: 100%; margin: 15px 0; }
  </style>
</head>
<body>
  <h1>🎧 Audio Trim Cutter</h1>
  <div class="box">
    <form method="POST" enctype="multipart/form-data">
      <p>Select audio file to trim:</p>
      <input type="file" name="audio" accept="audio/*" required><br>
      <label>Start (sec):</label>
      <input type="number" name="start" min="0" value="0" required>
      <label>End (sec):</label>
      <input type="number" name="end" min="1" value="10" required><br>
      <button type="submit">Trim Audio</button>
    </form>

    {% if audio_path %}
      <h3>Preview Trimmed Audio:</h3>
      <audio controls>
        <source src="{{ url_for('static', filename=audio_path) }}" type="audio/mp3">
      </audio><br>
      <a href="{{ url_for('static', filename=audio_path) }}" download>
        ⬇️ Download Trimmed Audio
      </a>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        audio = request.files["audio"]
        start = request.form["start"]
        end = request.form["end"]

        input_path = "input.mp3"
        output_path = os.path.join("static", "trimmed.mp3")
        audio.save(input_path)

        ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        command = [
            ffmpeg_path,
            "-i", input_path,
            "-ss", str(start),
            "-to", str(end),
            "-acodec", "copy",
            output_path
        ]
        subprocess.run(command)

        os.remove(input_path)
        return render_template_string(HTML_PAGE, audio_path="trimmed.mp3")

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
