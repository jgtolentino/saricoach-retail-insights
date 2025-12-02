import os
from gtts import gTTS

def text_to_speech(text: str, filename: str = "output.mp3", lang: str = "en"):
    """
    Converts text to an MP3 file using Google Translate's TTS API.
    """
    print(f"🎤 Generating audio for: '{text[:30]}...'")
    
    try:
        # Create the TTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save the file
        save_path = os.path.join("data", "audio", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        tts.save(save_path)
        print(f"✅ Audio saved to: {save_path}")
        
        # Optional: Play immediately (macOS/Linux only)
        # os.system(f"afplay {save_path}") 
        
    except Exception as e:
        print(f"❌ Error generating audio: {e}")

if __name__ == "__main__":
    # Example usage for SariCoach
    coach_message = (
        "Magandang umaga! Revenue is up 12% today. "
        "Don't forget to restock Coke Zero before the 5 PM rush."
    )
    text_to_speech(coach_message, filename="coach_briefing.mp3")
