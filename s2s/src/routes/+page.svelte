<script lang="ts">
  import { onMount } from 'svelte';

  let recording = false;
  let mediaRecorder;
  let audioChunks = [];
  let audioUrl = '';
  let message = '';
  let volumeLevel = 0; // This will control the movement

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    source.connect(analyser);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function updateVolume() {
      analyser.getByteFrequencyData(dataArray);
      volumeLevel = Math.max(...dataArray) / 255; // Normalize between 0 and 1
      requestAnimationFrame(updateVolume);
    }

    updateVolume();

    mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      sendAudioToBackend(audioBlob);
    };

    mediaRecorder.start();
    recording = true;
  }

  function stopRecording() {
    mediaRecorder.stop();
    recording = false;
  }

  async function sendAudioToBackend(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    const response = await fetch('http://localhost:5000/process-audio', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    message = result.text;

    const byteArray = new Uint8Array(
      result.audio.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
    );
    const audioBlobFromHex = new Blob([byteArray], { type: 'audio/mp3' });
    audioUrl = URL.createObjectURL(audioBlobFromHex);

    const audio = new Audio(audioUrl);
    const audioContext = new AudioContext();
    const source = audioContext.createMediaElementSource(audio);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    source.connect(analyser);
    source.connect(audioContext.destination);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function updateOutputVolume() {
      analyser.getByteFrequencyData(dataArray);
      volumeLevel = Math.max(...dataArray) / 255;
      requestAnimationFrame(updateOutputVolume);
    }

    updateOutputVolume();
    audio.play();
  }
</script>

<style>
  .chat-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .visualizer {
    width: 50px;
    height: 50px;
    background-color: blue;
    border-radius: 50%;
    transition: transform 0.1s linear;
    margin: 20px auto;
  }
</style>

<div class="chat-container p-4">
  <h2 class="text-xl font-bold mb-4">🎙️ Speech-to-Speech Chat</h2>
  
  <button 
    class="px-4 py-2 rounded-lg bg-blue-500 text-white" 
    on:click={recording ? stopRecording : startRecording}>
    {recording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
  </button>

  <div class="visualizer" style="transform: scale({volumeLevel + 0.5});"></div>

  {#if message}
    <p class="mt-4">📝 Recognized Text: <strong>{message}</strong></p>
  {/if}

  {#if audioUrl}
    <audio class="mt-4" controls>
      <source src={audioUrl} type="audio/mp3">
      Your browser does not support the audio element.
    </audio>
  {/if}
</div>
