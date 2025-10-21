# tts.py
import time
import os
from TTS.api import TTS
import pygame

# Model setup
model_name = "tts_models/en/ljspeech/vits"
tts = TTS(model_name=model_name, gpu=False)  # CPU mode

# Input (from Gemini/chat output) and Output (speech file)
input_file = "chat_output.txt"
audio_file = "coqui_output_fast.wav"

# Initialize pygame mixer for audio playback
pygame.mixer.init()

last_mtime = None


def play_audio(file_path):
    """Play audio using pygame mixer"""
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # Wait until audio finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        print(f"✅ Played: {file_path}")
    except Exception as e:
        print(f"⚠️ Error playing audio: {e}")


print("🔄 Watching for changes in chat_output.txt ...")
while True:
    try:
        if os.path.exists(input_file):
            mtime = os.path.getmtime(input_file)
            if last_mtime is None:
                last_mtime = mtime

            if mtime != last_mtime:  # File has changed
                with open(input_file, "r") as f:
                    text = f.read().strip()

                last_mtime = mtime

                if text:
                    print(f"🎤 Synthesizing: {text}")
                    
                    # Generate speech
                    tts.tts_to_file(text=text, file_path=audio_file)
                    
                    # Play audio
                    play_audio(audio_file)

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("⏹️ Stopped by user.")
        pygame.mixer.quit()
        break
