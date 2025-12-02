import os
from moviepy import VideoFileClip, ImageClip, concatenate_videoclips

# Configuration
INPUT_VIDEO = "docs/saricoach_demo.mp4" 
INPUT_IMAGE = "public/og-card.png"
OUTPUT_FILE = "docs/saricoach_demo.gif"
TARGET_WIDTH = 800
INTRO_DURATION = 2.0  # Seconds to show the OG card

def convert_to_gif():
    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Input video {INPUT_VIDEO} not found.")
        return
    if not os.path.exists(INPUT_IMAGE):
        print(f"❌ Input image {INPUT_IMAGE} not found.")
        return

    print(f"🔄 Loading assets...")
    video_clip = VideoFileClip(INPUT_VIDEO)
    
    # Create intro clip from image
    intro_clip = (ImageClip(INPUT_IMAGE)
                 .with_duration(INTRO_DURATION)
                 .resized(width=video_clip.w)) # Match video width for concatenation
                 
    # Concatenate
    print("➕ Prepending OG Card intro...")
    final_clip = concatenate_videoclips([intro_clip, video_clip])
    
    # Resize and optimize
    print(f"📉 Resizing to {TARGET_WIDTH}px width and optimizing palette...")
    optimized_clip = final_clip.resized(width=TARGET_WIDTH)
    
    # Create the docs directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print("💾 Writing GIF (this might take a minute)...")
    optimized_clip.write_gif(
        OUTPUT_FILE, 
        fps=15,             # Lower FPS for smaller file size
    )
    
    print(f"✅ Done! GIF saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    convert_to_gif()
