from flask import Flask, request, jsonify, send_file
import whisper
from gtts import gTTS
from flask_cors import CORS
from transformers import pipeline
from llama_cpp import Llama
import torch

app = Flask(__name__)
CORS(app)  
model = whisper.load_model("base")

llm = Llama.from_pretrained(
	repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
	filename="llama-2-7b-chat.Q2_K.gguf",
)


def comp(PROMPT, MaxToken=50, outputs=3):
    response = llm(PROMPT, max_tokens=MaxToken, n=outputs, stop=["\n"])
    return [resp["text"].strip() for resp in response["choices"]]


@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio']
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    # Transcribe audio to text  
    result = model.transcribe(audio_path)
    text = result["text"]
    
    # Generate AI response using Llama
    output = llm(
        text,
        max_tokens=512,
        echo=True
    )
    
    # Convert AI response to speech
    tts = gTTS(output, lang='en')
    output_audio_path = "output.mp3"
    tts.save(output_audio_path)
    
    with open(output_audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    return jsonify({"text": text, "ai_response": output, "audio": audio_data.hex()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
