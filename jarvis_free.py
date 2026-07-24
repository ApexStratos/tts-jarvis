import speech_recognition as sr
import ollama
import pyttsx3

# Initialize the local text-to-speech engine
engine = pyttsx3.init()

# Optional: Customize voice rate (speed) and volume
engine.setProperty('rate', 175)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Optional: Select a specific voice if available (Mac usually has 'Alex' or 'Victoria', etc.)
voices = engine.getProperty('voices')
for voice in voices:
    if "en_US" in voice.id or "Alex" in voice.id:
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    """Converts text to speech locally and offline using Mac's speech synthesis."""
    print(f"\n[Jarvis speaks]: {text}")
    engine.say(text)
    engine.runAndWait()

# Define Jarvis's persona
SYSTEM_PROMPT = (
    "You are Jarvis, an advanced, highly intelligent, and slightly sarcastic AI assistant "
    "inspired by Tony Stark's system. Keep your answers concise, witty, and optimized for a terminal interface."
)

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def listen_to_mic():
    """Listens to the microphone and converts speech to text locally."""
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
        except sr.WaitTimeoutError:
            print("[Listening timed out]")
            return None
        except sr.UnknownValueError:
            print("[Could not understand audio]")
            return None
        except Exception as e:
            print(f"[Mic Error]: {e}")
            return None

def ask_local_jarvis(user_input):
    """Sends input to your local Ollama model (llama3) for free token processing."""
    conversation_history.append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(model='llama3', messages=conversation_history)
        reply = response['message']['content']
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Sir, my local neural link encountered a glitch: {e}"

def main():
    print("=" * 50)
    print(" FREE LOCAL JARVIS TERMINAL ONLINE")
    print("=" * 50)
    speak("Jarvis online. Systems nominal. Local processing active. How may I assist you today, sir?")

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
            print("Invalid selection. Please choose 't', 'v', or 'q'.")
            continue

        if user_input:
            reply = ask_local_jarvis(user_input)
            print(f"\nJarvis (Text): {reply}")
            speak(reply)

if __name__ == "__main__":
    main()
