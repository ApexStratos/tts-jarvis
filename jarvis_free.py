import os
import subprocess
import speech_recognition as sr
import ollama
import pyttsx3

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"\n[Jarvis speaks]: {text}")
    engine.say(text)
    engine.runAndWait()

# --- CLAUDE-LIKE TOOLS ---
def run_terminal_command(command):
    """Executes a shell command on your Mac and returns the output."""
    print(f"\n[Jarvis Tool]: Executing command -> {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Failed to execute command: {e}"

def read_local_file(filepath):
    """Reads a local file's content."""
    print(f"\n[Jarvis Tool]: Reading file -> {filepath}")
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

# Map tool names to actual functions
available_tools = {
    'run_terminal_command': run_terminal_command,
    'read_local_file': read_local_file
}

# System prompt defining Claude-like assistant behavior and tool access
SYSTEM_PROMPT = (
    "You are Jarvis, an advanced local AI assistant with capabilities similar to Claude. "
    "You are helpful, precise, and capable of executing actions. "
    "If the user asks you to run a terminal command, check files, or perform local actions, "
    "you can use your tools. Keep responses concise for a terminal interface."
)

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening... Speak now]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            print("[Processing voice...]")
            text = r.recognize_google(audio)
            print(f"You (Voice): {text}")
            return text
        except Exception:
            print("[Could not understand audio or timed out]")
            return None

def ask_local_jarvis(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    try:
        # Using qwen2.5-coder for high-tier local reasoning & coding capability
        response = ollama.chat(
            model='qwen2.5-coder:7b', 
            messages=conversation_history
        )
        reply = response['message']['content']
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Sir, my local neural link encountered a glitch: {e}"

def main():
    print("=" * 50)
    print(" CLAUDE-POWERED LOCAL JARVIS ONLINE")
    print("=" * 50)
    speak("Jarvis online. Systems nominal. Advanced capabilities active. How may I assist you, sir?")

    while True:
        print("\nOptions:")
        print("  [t] Type a message")
        print("  [v] Speak via microphone")
        print("  [q] Quit")

        choice = input("\nSelect input mode (t/v/q): ").strip().lower()
        user_input = ""

        if choice == 't':
            user_input = input("\nYou (Text): ").strip()
            if user_input.lower() == 'quit':
                break
        elif choice == 'v':
            user_input = listen_to_mic()
        elif choice == 'q':
            speak("Powering down, sir. Goodbye.")
            break
        else:
            print("Invalid selection.")
            continue

        if user_input:
            reply = ask_local_jarvis(user_input)
            print(f"\nJarvis (Text): {reply}")
            speak(reply)

if __name__ == "__main__":
    main()
