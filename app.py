# app.py - Only Landing Page Updated
import gradio as gr
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import time
import os

# --- Load Custom & Tailwind CSS ---
def load_css():
    css = """
    /* Custom CSS for modern look */
    body, #root { background-color: #0A0A0A; color: #E2E2E2; font-family: 'Inter', sans-serif; }
    .gradio-container { background: transparent; box-shadow: none !important; }
    footer { display: none !important; }
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { background: #7C3AED; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #9333ea; }
    """
    tailwind_css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/output.css")
    try:
        with open(tailwind_css_path, "r", encoding="utf-8") as f:
            tailwind_css = f.read()
        return tailwind_css + css
    except FileNotFoundError:
        print("Warning: static/output.css not found. The UI will not be styled correctly.")
        return css

# ----------------- Parameters (CPU Optimized) -----------------
SAMPLE_RATE = 16000
CHUNK_DURATION = 0.5
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
MODEL_SIZE = "tiny.en"
DEVICE = "cpu"
BEAM_SIZE = 15
TEMPERATURE = 0.0
COMPUTE_TYPE = "int8"

# ----------------- Initialize model -----------------
print("Loading Whisper model...")
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    model = None

# ----------------- Global state -----------------
recording = False
audio_buffer = []

# ----------------- Audio callback -----------------
def callback(indata, frames, time_info, status):
    global recording
    if recording:
        audio_buffer.append(indata[:, 0].astype(np.float32))

# ----------------- UI Helper Functions -----------------
def create_status_display(status_text):
    return f"""
    <div class="p-4 text-center rounded-lg bg-neutral-800 border-neutral-700">
        <p class="text-2xl font-bold text-white tracking-wider uppercase">Status</p>
        <p class="text-lg text-neutral-300 mt-1">{status_text}</p>
    </div>
    """

# ----------------- Core Transcription Logic -----------------
def start_recording():
    global recording, audio_buffer
    audio_buffer = []
    recording = True
    return create_status_display("Recording..."), "..."

def stop_recording():
    global recording, audio_buffer
    if not recording: 
        return create_status_display("Not Recording"), ""
    
    recording = False
    sd.sleep(int(CHUNK_DURATION * 1000))
    
    if not audio_buffer: 
        return create_status_display("No Audio"), ""

    audio_data = np.concatenate(audio_buffer)
    audio_buffer = []
    
    if model is None: 
        return create_status_display("Model Error"), ""

    print("Transcribing...")
    segments, _ = model.transcribe(audio_data, beam_size=BEAM_SIZE, temperature=TEMPERATURE)
    transcription_text = "\n".join(segment.text for segment in segments)

    filename = "input.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcription_text)
    
    return create_status_display("Complete"), transcription_text

# ----------------- Page Navigation -----------------
def navigate_to_interview():
    return {
        landing_page: gr.update(visible=False), 
        interview_page: gr.update(visible=True), 
        feedback_page: gr.update(visible=False)
    }

def navigate_to_feedback():
    global recording
    recording = False
    return {
        landing_page: gr.update(visible=False), 
        interview_page: gr.update(visible=False), 
        feedback_page: gr.update(visible=True)
    }

def submit_feedback_and_reset(rating, feedback_text):
    print(f"--- Feedback ---\nRating: {rating}\nComments: {feedback_text}\n----------------")
    return {
        feedback_page: gr.update(visible=False), 
        landing_page: gr.update(visible=True), 
        interview_page: gr.update(visible=False),
        feedback_rating: gr.update(value=None), 
        feedback_comments: gr.update(value="")
    }

def clear_transcription():
    return create_status_display("Idle"), ""

# ----------------- Start audio stream -----------------
try:
    stream = sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=callback, blocksize=CHUNK_SIZE)
    stream.start()
    print("Audio stream started.")
except Exception as e:
    print(f"Error initializing audio stream: {e}")

# ----------------- Gradio Interface -----------------
with gr.Blocks(css=load_css(), elem_classes="min-h-screen") as demo:

    # ============================================================
    # === 1. LANDING PAGE (UPDATED - Modern Design) ===
    # ============================================================
    with gr.Column(visible=True, elem_classes="items-center") as landing_page:
        # Hero Section with Gradient Background
        gr.HTML("""
        <div class="w-full flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8 overflow-hidden animate-in fade-in duration-1000">
            <div class="absolute top-0 left-0 w-full h-full bg-[#0A0A0A] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]"></div>
            <div class="absolute inset-0 z-0 h-full w-full bg-[#0A0A0A] bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]"></div>
            <div class="z-10 text-center">
                <h1 class="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400 bg-opacity-50">
                    Your AI Interview Coach
                </h1>
                <p class="mt-4 text-lg text-neutral-300 max-w-2xl mx-auto">
                    Sharpen your skills with real-time transcription and analysis. Practice makes perfect.
                </p>
            </div>
        </div>
        """)
        
        # Centered Call-to-Action Button (Smaller)
        with gr.Row(elem_classes="flex justify-center mt-8 mb-16 z-10 w-full"):
            try_interview_btn = gr.Button(
                "🚀 Try the Interview Experience", 
                elem_classes="px-8 py-3 rounded-full text-base font-bold text-white bg-purple-600 hover:bg-purple-700 transition-all transform hover:scale-105 shadow-lg shadow-purple-900/50"
            )

        # Bento Grid - Feature Cards
        gr.HTML("""
        <div class="z-10 max-w-6xl w-full grid grid-cols-1 md:grid-cols-4 gap-6 animate-in fade-in-0 slide-in-from-bottom-12 duration-1000 px-4">
            <!-- Large Card: Real-Time Transcription -->
            <div class="md:col-span-2 md:row-span-2 p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl flex flex-col justify-between backdrop-blur-sm hover:border-purple-500/80 transition-colors">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" x2="12" y1="19" y2="22"></line></svg>
                    <h3 class="text-2xl font-semibold text-white mt-4">Real-Time Transcription</h3>
                    <p class="text-neutral-400 mt-2">See your words appear on screen. Identify filler words and improve your articulation instantly.</p>
                </div>
                <div class="mt-4 w-full p-4 bg-black rounded-lg border border-neutral-700 h-36 text-left font-mono text-sm text-green-400 overflow-y-auto">
                    &gt; User: "Uhm, so, my greatest strength is... well, I believe it's my ability to, like, collaborate effectively with diverse teams."<br>
                    &gt; AI Suggestion: "My greatest strength is my ability to collaborate effectively with diverse teams."
                </div>
            </div>
            
            <!-- Card: Boost Confidence -->
            <div class="md:col-span-2 p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl flex flex-col backdrop-blur-sm hover:border-purple-500/80 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                <h3 class="text-2xl font-semibold text-white mt-4">Boost Confidence</h3>
                <p class="text-neutral-400 mt-2">Practice common interview questions until your answers are crisp, confident, and natural.</p>
            </div>
            
            <!-- Card: Save & Review -->
            <div class="p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl flex flex-col backdrop-blur-sm hover:border-purple-500/80 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
                <h3 class="text-2xl font-semibold text-white mt-4">Save & Review</h3>
                <p class="text-neutral-400 mt-2">All your practice sessions are saved to track progress.</p>
            </div>
            
            <!-- Card: User Approved -->
            <div class="p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl flex flex-col backdrop-blur-sm hover:border-purple-500/80 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                <h3 class="text-2xl font-semibold text-white mt-4">User Approved</h3>
                <p class="text-neutral-400 mt-2 italic">"This was a game-changer. I got the job!" - Alex J.</p>
            </div>
        </div>
        """)

    # ============================================================
    # === 2. INTERVIEW PAGE (UNCHANGED - Your Original) ===
    # ============================================================
    with gr.Column(visible=False, elem_classes="w-full min-h-screen flex items-center justify-center p-4 animate-in fade-in duration-500") as interview_page:
        with gr.Row(elem_classes="w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8"):
            # Left Column: Controls & Status
            with gr.Column(elem_classes="lg:col-span-1 space-y-6"):
                gr.Markdown("""
                <div class="p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl backdrop-blur-sm">
                    <h2 class="text-3xl font-bold text-white">Controls</h2>
                    <p class="text-neutral-400 mt-2">Manage your recording session here.</p>
                </div>
                """)
                status = gr.HTML(create_status_display("Idle"))
                with gr.Column(elem_classes="p-6 bg-neutral-900/80 border border-neutral-800 rounded-2xl backdrop-blur-sm space-y-4"):
                    start_button = gr.Button("▶️ Start Recording", elem_classes="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg text-xl shadow-lg transform hover:scale-105 transition-all")
                    stop_button = gr.Button("⏹️ Stop Recording", elem_classes="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-lg text-xl shadow-lg transform hover:scale-105 transition-all")
                    clear_button = gr.Button("🗑️ Clear Transcript", elem_classes="w-full bg-neutral-600 hover:bg-neutral-700 text-white font-bold py-3 px-4 rounded-lg text-xl shadow-lg transform hover:scale-105 transition-all")
                end_interview_btn = gr.Button("🏁 End Interview & Give Feedback", elem_classes="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 rounded-lg text-xl shadow-lg transform hover:scale-105 transition-all")

            # Right Column: Transcription Output
            with gr.Column(elem_classes="lg:col-span-2"):
                with gr.Column(elem_classes="p-8 bg-neutral-900/80 border border-neutral-800 rounded-2xl backdrop-blur-sm h-full"):
                    gr.Markdown("""
                    <h2 class="text-3xl font-bold text-white">Live Transcription</h2>
                    <p class="text-neutral-400 mt-2">Your spoken words will appear here in real-time.</p>
                    """)
                    transcription_output = gr.Textbox(
                        label="Your Response", 
                        lines=20, 
                        interactive=False, 
                        placeholder="Transcription will appear here...", 
                        elem_classes="mt-4 p-4 rounded-lg bg-black/50 border border-neutral-700 text-lg leading-relaxed text-neutral-200 w-full h-full font-mono"
                    )

    # ============================================================
    # === 3. FEEDBACK PAGE (UNCHANGED - Your Original) ===
    # ============================================================
    with gr.Column(visible=False, elem_classes="w-full min-h-screen flex flex-col items-center justify-center animate-in fade-in duration-500") as feedback_page:
        with gr.Column(elem_classes="max-w-2xl mx-auto p-8 bg-neutral-900/80 border border-neutral-800 rounded-2xl backdrop-blur-sm"):
            gr.Markdown("""
            <div class="text-center">
                <h1 class="text-4xl font-bold text-white">Interview Complete!</h1>
                <p class="text-neutral-400 mt-2">Your feedback helps us improve.</p>
            </div>
            """)
            feedback_rating = gr.Radio(
                ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], 
                label="How would you rate your experience?", 
                elem_classes="mt-6 text-2xl font-semibold"
            )
            feedback_comments = gr.Textbox(
                label="Any additional comments?", 
                lines=5, 
                placeholder="What did you like? What could be improved?", 
                elem_classes="mt-4 p-4 rounded-lg bg-black/50 border border-neutral-700 text-lg leading-relaxed text-neutral-200"
            )
            submit_feedback_btn = gr.Button(
                "Submit Feedback", 
                elem_classes="mt-6 w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg text-xl shadow-lg transform hover:scale-105 transition-all"
            )

    # --- Event Handlers (Unchanged) ---
    try_interview_btn.click(
        fn=navigate_to_interview, 
        inputs=None, 
        outputs=[landing_page, interview_page, feedback_page]
    )
    end_interview_btn.click(
        fn=navigate_to_feedback, 
        inputs=None, 
        outputs=[landing_page, interview_page, feedback_page]
    )
    submit_feedback_btn.click(
        fn=submit_feedback_and_reset, 
        inputs=[feedback_rating, feedback_comments], 
        outputs=[landing_page, interview_page, feedback_page, feedback_rating, feedback_comments]
    )
    start_button.click(fn=start_recording, outputs=[status, transcription_output])
    stop_button.click(fn=stop_recording, outputs=[status, transcription_output])
    clear_button.click(fn=clear_transcription, outputs=[status, transcription_output])

if __name__ == "__main__":
    demo.launch()
