from flask import Flask, render_template, request, send_from_directory
import fitz
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file uploaded"

        file = request.files["pdf"]

        if file.filename == "":
            return "No selected file"

        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            text += page.get_text()

        if not text.strip():
            return "No readable text found in PDF"

        # unique filename (important for Render)
        filename = f"{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text)
        tts.save(audio_path)

        return send_from_directory(AUDIO_FOLDER, filename, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)