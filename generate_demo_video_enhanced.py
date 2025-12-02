import os
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, vfx
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 1. Configuration
OUTPUT_FILE = "saricoach_demo_enhanced.mp4"
FPS = 24
IMAGE_DIR = "public"
AUDIO_DIR = "data/audio_temp"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 2. Storyboard: Image, Script, and Title
storyboard = [
    {
        "image": "Screenshot 2025-12-02 at 4.09.48 PM.png",
        "title": "Real-Time Dashboard",
        "script": "Welcome to Sari Coach. This is your real-time dashboard showing daily revenue and traffic."
    },
    {
        "image": "Screenshot 2025-12-02 at 4.10.13 PM.png",
        "title": "Weekly Insights",
        "script": "Track your weekly performance. See which days are busiest and optimize your staffing."
    },
    {
        "image": "Screenshot 2025-12-02 at 4.10.22 PM.png",
        "title": "Transaction History",
        "script": "Review every transaction. Spot trends and identify your best-selling items instantly."
    },
    {
        "image": "Screenshot 2025-12-02 at 4.10.33 PM.png",
        "title": "Store Settings",
        "script": "Configure your store profile and preferences to get personalized coaching advice."
    },
    {
        "image": "Screenshot 2025-12-02 at 4.10.44 PM.png",
        "title": "AI Coach Chat",
        "script": "Ask the AI Coach anything. It analyzes your data to give you specific, actionable advice."
    },
    {
        "image": "Screenshot 2025-12-02 at 4.19.39 PM.png",
        "title": "Mobile First",
        "script": "Designed for mobile. Manage your store from anywhere, right from your pocket."
    }
]

def add_text_to_image(img_path, title):
    """Draws a title bar on the image using PIL"""
    with Image.open(img_path) as img:
        # Convert to RGB
        img = img.convert("RGB")
        
        # Resize to standard width (1920)
        base_width = 1920
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        
        # Draw semi-transparent bar at bottom
        # Since PIL doesn't support alpha on RGB directly for drawing, we blend
        # But for simplicity, let's just draw a solid bar or use a simple hack
        # We'll draw a solid dark bar at the bottom
        bar_height = 120
        draw.rectangle([(0, h_size - bar_height), (base_width, h_size)], fill=(0, 0, 0))
        
        # Draw Text
        try:
            # Try to load a standard font
            font = ImageFont.truetype("Arial.ttf", 60)
        except:
            # Fallback to default
            font = ImageFont.load_default()
            
        # Center text
        # getbbox returns (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (base_width - text_width) / 2
        y = h_size - bar_height + (bar_height - text_height) / 2 - 10 # Adjust for baseline
        
        draw.text((x, y), title, font=font, fill=(255, 255, 255))
        
        return np.array(img)

def create_enhanced_video():
    print("🎬 Starting Enhanced Video Generation...")
    clips = []

    for item in storyboard:
        img_name = item["image"]
        img_path = os.path.join(IMAGE_DIR, img_name)
        
        if not os.path.exists(img_path):
            print(f"⚠️ Skipping missing image: {img_name}")
            continue

        print(f"Processing: {item['title']}")

        # 1. Generate Audio
        audio_filename = f"{img_name}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        tts = gTTS(text=item["script"], lang="en", slow=False)
        tts.save(audio_path)
        
        # Load Audio Clip
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + 0.5 # Add a little pause

        # 2. Process Image (Resize + Text)
        img_array = add_text_to_image(img_path, item["title"])
        
        # 3. Create Video Clip
        clip = (ImageClip(img_array)
                .with_duration(duration)
                .with_audio(audio_clip)
                .with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.5)]))
        
        clips.append(clip)

    if not clips:
        print("❌ No clips created.")
        return

    # 4. Concatenate
    print("✨ Stitching video...")
    final_video = concatenate_videoclips(clips, method="compose", padding=-0.5)

    # 5. Write File
    print(f"💾 Saving to {OUTPUT_FILE}...")
    final_video.write_videofile(
        OUTPUT_FILE, 
        fps=FPS, 
        codec="libx264", 
        audio_codec="aac",
        preset="medium"
    )
    print("✅ Done!")

if __name__ == "__main__":
    create_enhanced_video()
