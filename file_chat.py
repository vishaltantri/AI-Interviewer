# file_chat.py
import time
import os
import re
from google import genai

# Get the API key from the environment variable
api_key = os.environ.get('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set! Please check your run_coach.sh script.")

input_file = "input.txt"
output_file = "chat_output.txt"

# ✅ CORRECT: Initialize client (SDK will use GOOGLE_API_KEY automatically)
client = genai.Client(api_key=api_key)

# 🔑 System instruction for the interviewer
system_instruction = (
    "You are a strict interviewer conducting a professional job interview. "
    "Your output must ONLY be what an interviewer would actually speak aloud. "
    "Do NOT include stage directions, emotions, or descriptions like '(clears throat)' or '(smiles)'. No Emoji. "
    "Every response you give must be a QUESTION or a feedback of answer or a proper response."
)

def clean_text(text):
    """Clean text for TTS compatibility"""
    text = text.replace("AI/ML", "AI and ML")
    text = re.sub(r"[\[\]\(\)\{\}<>]", "", text)  # remove brackets/parentheses
    text = text.replace("/", " and ")  # general slash replacement
    text = text.replace('"', "")       # remove quotes
    text = text.replace("—", "-")      # normalize dashes
    text = text.replace("\n", " ")     # merge multiple lines
    text = re.sub(r"\s+", " ", text).strip()  # collapse multiple spaces
    return text

# ✅ CORRECT: Create chat session using client.chats.create()
# This is the proper way according to the official SDK documentation
chat = client.chats.create(
    model='gemini-2.0-flash-exp',
    config={
        'system_instruction': system_instruction,
        'temperature': 0.7,
    }
)

last_mtime = None  # To track file changes

def read_input():
    """Reads the full input file content."""
    if not os.path.exists(input_file):
        return None
    with open(input_file, "r") as f:
        return f.read().strip()

def write_response(text):
    """Writes the AI's response to the output file."""
    with open(output_file, "w") as f:
        f.write(text + "\n")

# Main loop
print("🔄 Watching input.txt ...")
while True:
    try:
        if os.path.exists(input_file):
            mtime = os.path.getmtime(input_file)  # last modified time
            if last_mtime is None:
                last_mtime = mtime

            if mtime != last_mtime:  # if file has changed
                user_message = read_input()
                last_mtime = mtime

                if user_message:
                    try:
                        # ✅ CORRECT: Use chat.send_message()
                        response = chat.send_message(user_message)
                        reply = response.text
                        
                        # 🔹 Clean Gemini output for TTS
                        reply = clean_text(reply)
                        
                        write_response(reply)
                        print(f"User: {user_message}\nGemini: {reply}\n")
                    except Exception as e:
                        print(f"⚠️ Error with Gemini API: {e}")

        time.sleep(1)

    except KeyboardInterrupt:
        print("⏹️ Stopped by user.")
        break
