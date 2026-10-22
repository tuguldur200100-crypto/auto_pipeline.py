import os
import subprocess
import whisper

# --- 1. COPYWRITER AGENT ---
def generate_hook_and_caption(transcript_text):
    """ Whisper-ийн текст дээр тулгуурлан Hook болон Caption автоматаар зохионо """
    words = transcript_text.strip().split()
    first_few_words = " ".join(words[:6]).upper() if words else "MUST WATCH!"
    
    # Вирал Hook (Дэлгэцэн дээр харагдах гарчиг)
    hook_text = f"WAIT FOR IT... 😱\n{first_few_words}"
    
    # Social Media Caption
    caption = f"{first_few_words}... 🔥 #viral #twitch #streamer #clips #fyp"
    
    return hook_text, caption

# --- 2. SUBTITLE & CROP AGENT (FFmpeg) ---
def process_video_with_subtitles(video_url, start_time, duration, output_file, hook_text):
    """ Video-г 9:16 болгож, дээд талд нь Hook текст наах FFmpeg command """
    
    # Текстэн доторх тусгай тэмдэгтүүдийг цэвэрлэх
    clean_hook = hook_text.replace("'", "").replace('"', '').replace(":", "")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", video_url,
        "-vf", (
            f"crop=ih*(9/16):ih,"  # 9:16 Босоо формат
            f"drawtext=text='{clean_hook}':x=(w-text_w)/2:y=100:" # Дээд хэсэгт Hook наах
            f"fontsize=24:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=5"
        ),
        "-c:a", "aac",
        "-b:a", "192k",
        output_file
    ]
    subprocess.run(ffmpeg_cmd, check=True)

# --- 3. VIRAL DETECTOR & SCRAPER AGENT ---
def get_best_viral_segment(audio_path):
    print("--- [Agent] Whisper AI дууг текст рүү хөрвүүлж байна... ---")
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    
    segments = result.get("segments", [])
    if not segments:
        return 0, 45, "CRAZY MOMENT"
    
    best_start = 0
    max_score = -1
    best_text = ""
    
    viral_keywords = ["omg", "wtf", "no way", "holy", "insane", "bro", "look", "yoo", "fuck", "shit"]
    
    for seg in segments:
        text = seg['text'].lower()
        score = len(text.split())
        for word in viral_keywords:
            if word in text:
                score += 20
                
        if score > max_score:
            max_score = score
            best_start = seg['start']
            best_text = seg['text']
            
    print(f"--- [Agent] Вирал оноо: {max_score} | Эхлэх хугацаа: {best_start}с ---")
    return best_start, 45, best_text

def run_pipeline():
    # Таны дагах 4-5 стримерийн жагсаалт
    STREAMERS = [
        {"name": "Streamer_1", "url": "https://www.youtube.com/watch?v=EXAMPLE_1"},
    ]
    
    for streamer in STREAMERS:
        print(f"\n==========================================")
        print(f"Processing Streamer: {streamer['name']}")
        print(f"==========================================")
        
        audio_temp = "temp_audio.mp3"
        
        try:
            # 1. Аудио татах
            subprocess.run([
                "yt-dlp", "-x", "--audio-format", "mp3",
                "-o", audio_temp, streamer["url"], "--force-overwrites"
            ], check=True)
            
            # 2. AI оноо тооцож, шилдэг хэсгийг олох
            start_time, duration, text_snippet = get_best_viral_segment(audio_temp)
            
            # 3. Copywriter Agent-аар Hook & Caption зохиох
            hook, caption = generate_hook_and_caption(text_snippet)
            print(f"--- [Copywriter Agent] Hook: {hook} ---")
            print(f"--- [Copywriter Agent] Caption: {caption} ---")
            
            # 4. 9:16 болгож хайчлан, дэлгэцэнд текст наах
            output_clip = f"{streamer['name']}_viral.mp4"
            process_video_with_subtitles(streamer["url"], start_time, duration, output_clip, hook)
            
            print(f"✅ Амжилттай бэлэн боллоо: {output_clip}")
            
        except Exception as e:
            print(f"❌ Алдаа гарлаа ({streamer['name']}): {e}")

if __name__ == "__main__":
    run_pipeline()
