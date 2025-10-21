import subprocess
import sys

# Programs to run
programs = [
    "file_chat.py",
    "app.py",
    "tts.py"
]

processes = []

try:
    for prog in programs:
        print(f"🔄 Starting {prog} ...")
        # run each in parallel
        p = subprocess.Popen([sys.executable, prog])
        processes.append(p)

    print("✅ All programs launched. Press CTRL+C to stop.")

    # Keep script alive until user interrupts
    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("\n⏹️ Stopping all programs...")
    for p in processes:
        p.terminate()