from flask import Flask, request, jsonify, send_file
import whisper
from gtts import gTTS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
model = whisper.load_model("base")

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio']
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    result = model.transcribe(audio_path)
    text = result["text"]
    
    tts = gTTS(text, lang='en')
    output_audio_path = "output.mp3"
    tts.save(output_audio_path)
    
    with open(output_audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    return jsonify({"text": text, "audio": audio_data.hex()})  

if __name__ == '__main__':
    app.run(debug=True, port=5000)
