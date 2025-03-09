<script lang="ts">
  let recording = false;
  let mediaRecorder;
  let audioChunks = [];
  let audioUrl = '';
  let message = '';

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

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

  async function sendAudioToBackend(audioBlob: Blob) {
  const formData = new FormData();
  formData.append('audio', audioBlob);

  const response = await fetch('http://localhost:5000/process-audio', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  message = result.text;

  // Convert hex-encoded audio back to a Blob
  const byteArray = new Uint8Array(
    result.audio.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
  );
  const audioBlobFromHex = new Blob([byteArray], { type: 'audio/mp3' });
  audioUrl = URL.createObjectURL(audioBlobFromHex);
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
  }
</style>

<div class="chat-container p-4">
  <h2 class="text-xl font-bold mb-4">🎙️ Speech-to-Speech Chat</h2>
  <button 
    class="px-4 py-2 rounded-lg bg-blue-500 text-white" 
    on:click={recording ? stopRecording : startRecording}>
    {recording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
  </button>
  
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
