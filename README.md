<div align="center">

# 🎤 AI Interview Coach

![Python](https://img.shields.io/badge/Python-3.10-blue.svg?logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.44-orange.svg?logo=gradio&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg?logo=linux&logoColor=white)

**Master your interview skills with real-time AI-powered transcription, feedback, and voice analysis**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## ✨ Features

- 🎙️ **Real-Time Transcription** - Accurate speech-to-text using Faster-Whisper
- 🤖 **AI Feedback** - Intelligent responses from Google Gemini 2.0
- 🔊 **Voice Synthesis** - Natural TTS using Coqui TTS
- 🎨 **Modern UI** - Beautiful Gradio interface with Tailwind CSS
- 💾 **Session Tracking** - Save and review practice sessions
- ⚡ **CPU Optimized** - Runs on standard hardware

---

## 📸 Demo

### Landing Page
<img src="https://github.com/user-attachments/assets/33ade9ab-3b26-471c-ba4a-11d2fa580445" alt="AI Interview Coach Landing Page" width="800">

*Modern gradient hero section with feature showcase and call-to-action*

### Interview Session
<img src="https://github.com/user-attachments/assets/75b8bfd2-214a-4294-b9ec-c8b761a89d23" alt="Live Interview Session" width="800">

*Real-time transcription with AI-powered feedback and voice synthesis*

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Linux (Fedora/Ubuntu/Debian)
- Google Gemini API Key ([Get free here](https://ai.google.dev/))

### Installation

Clone repository
git clone https://github.com/YOUR_USERNAME/ai-interviewer.git
cd ai-interviewer

Create virtual environment
python3.10 -m venv ai-coach-env
source ai-coach-env/bin/activate

Install dependencies
pip install -r requirements.txt

Configure API key
nano run_coach.sh

Replace YOUR_API_KEY_HERE with your actual Gemini API key
Make executable
chmod +x run_coach.sh

Launch application
./run_coach.sh

text

Open browser: [**http://127.0.0.1:7860**](http://127.0.0.1:7860)

---

## 🎯 Usage

1. Click **"🚀 Try the Interview Experience"** on the landing page
2. Press **"▶️ Start Recording"** and speak your answer clearly
3. Press **"⏹️ Stop Recording"** when finished
4. AI will transcribe, analyze, and provide feedback
5. Listen to the AI's spoken response
6. Continue the conversation or click **"🏁 End Interview"**

### Example Interaction

👤 You: "My greatest strength is problem-solving. I enjoy breaking down
complex challenges into manageable steps and finding creative solutions."

🤖 AI: "That's a valuable skill. Can you provide a specific example where you
successfully used problem-solving to overcome a difficult situation?"

text

---

## 📁 Project Structure

ai-interviewer/
├── app.py # Gradio UI + Whisper transcription
├── file_chat.py # Gemini AI conversation logic
├── tts.py # Coqui TTS audio synthesis
├── main.py # Multi-process orchestrator
├── run_coach.sh # Launch script with environment setup
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
├── input.css # Tailwind CSS source
└── static/
└── output.css # Compiled Tailwind CSS

text

---

## ⚙️ Configuration

### Change Whisper Model

Edit `app.py` (line 39):
MODEL_SIZE = "base.en" # Options: tiny.en, base.en, small.en, medium.en

text

**Model Comparison:**

| Model | Accuracy | Speed | Memory |
|-------|----------|-------|--------|
| tiny.en | ~95% | Fastest | 75 MB |
| base.en | ~98% | Fast | 140 MB |
| small.en | ~99% | Medium | 460 MB |

### Change Gemini Model

Edit `file_chat.py` (line 40):
model='gemini-2.0-flash-exp' # Or: gemini-1.5-pro, gemini-1.5-flash

text

---

## 🐛 Troubleshooting

### No audio output?
pip install --force-reinstall pygame
speaker-test -t wav -c 2

text

### Model download fails?
rm -rf ~/.cache/huggingface/
rm -rf ~/.local/share/tts/
./run_coach.sh

text

### API authentication error?
- Verify API key in `run_coach.sh` (no extra spaces)
- Check key validity at [Google AI Studio](https://ai.google.dev/)
- Ensure key has proper permissions

### Poor transcription accuracy?
- Upgrade to `base.en` or `small.en` model
- Speak clearly at normal pace
- Minimize background noise
- Position microphone 6-12 inches away

---

## 🛠️ Tech Stack

- **[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)** - Optimized OpenAI Whisper for speech recognition
- **[Google Gemini 2.0](https://ai.google.dev/)** - Advanced conversational AI model
- **[Coqui TTS](https://github.com/coqui-ai/TTS)** - Neural text-to-speech synthesis
- **[Gradio 4.x](https://gradio.app/)** - Modern Python web UI framework
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **sounddevice, pygame** - Real-time audio I/O

---

## 🗺️ Roadmap

- [ ] Multi-language interview support
- [ ] Custom question bank uploads
- [ ] Performance analytics dashboard
- [ ] Video recording for body language analysis
- [ ] Cloud deployment option
- [ ] Mobile app (iOS/Android)
- [ ] Resume-based question generation

---

## 🙏 Acknowledgments

- **OpenAI** - For the Whisper speech recognition model
- **Google** - For Gemini API access and support
- **Coqui AI** - For open-source TTS technology
- **Gradio Team** - For the amazing UI framework
- **SYSTRAN** - For Faster-Whisper optimization

---

## 📧 Contact

**VISHAL C TANTRI**  
GitHub: [@vishaltantri](https://github.com/vishaltantri)  
Project Link: [https://github.com/vishaltantri/AI-Interviewer/](https://github.com/vishaltantri/AI-Interviewer/)

---

<div align="center">

**Built with ❤️ for interview success**

⭐ Star this repo if you find it useful!

</div>
