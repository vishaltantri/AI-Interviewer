#!/bin/bash

# --- 1. Automated Cleanup (Prevents "device busy" errors) ---
echo "--- Performing old process cleanup ---"
# Kills any running processes that contain the names of our main files
pkill -f 'app.py|tts.py|file_chat.py'
echo "Cleanup complete."
echo "--------------------------------------"
echo ""

# --- 2. Activate Virtual Environment ---
# Ensures we use the correct Python version and libraries
source ai-coach-env/bin/activate

# --- 3. Set Environment Variables (API Key) ---
# 🚨 IMPORTANT: REPLACE YOUR_API_KEY_HERE with your actual Gemini API Key
export GOOGLE_API_KEY=AIzaSyBIoTh8Fjfki7ZFxY2lF1rzVjdUd7TVa40

# --- 4. Launch the Application ---
echo "Launching AI Interview Coach (app.py, file_chat.py, tts.py)..."
python main.py