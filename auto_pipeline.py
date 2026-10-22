import os
import subprocess
import whisper

def get_best_viral_segment(audio_path):
    print("--- [AI Agent] Whisper ашиглан дууг текст рүү хөрвүүлж байна... ---")
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    
    segments = result.get("segments", [])
    if not segments:
        return 0, 45 # Хэрэв текст олдохгүй бол эхний 45 секийг авна
    
    best_start = 0
    max_score = -1
    
    # AI Шинжилгээ: Хамгийн их энергитэй, яриа ихтэй хэсгийг хайна
    for i in range(len(segments)):
        current_text = segments[i]['text'].lower()
        score = len(current_text.split()) # Үгийн тоогоор ярианы идэвхийг хэмжих
        
        # Вирал болох магадлалтай түлхүүр үгсд бонус бал өгөх
        viral_keywords = ["omg", "wtf", "no way", "holy", "insane", "bro", "look", "yoo"]
        for word in viral_keywords:
            if word in current_text:
                score += 15
                
        if score > max_score:
            max_score = score
            best_start = segments[i]['start']
            
    print(f"--- [AI Agent] Хамгийн өндөр Viral Score-той хэсэг олоход: {best_start} сек-ээс эхэлж байна ---")
    return best_start, 45

def process_streamers():
    STREAMERS = [
        {"name": "Streamer1", "url": "https://www.youtube.com/watch?v=EXAMPLE_1"}
    ]
    
    for streamer in STREAMERS:
        print(f"\nProcessing: {streamer['name']}")
        
        # 1. Стримийг бүхлээр нь эсвэл хэсгийг нь аудио хэлбэрээр татах
        audio_file = "temp_audio.mp3"
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "-o", audio_file, streamer["url"], "--force-overwrites"
        ], check=True)
        
        # 2. AI-аар вирал хэсгийг олох
        start_time, duration = get_best_viral_segment(audio_file)
        
        # 3. Олдсон вирусын оноо өндөртэй хэсгийг FFmpeg-ээр 9:16 тайрч авах
        output_clip = f"{streamer['name']}_viral_clip.mp4"
        crop_cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-t", str(duration),
            "-i", streamer["url"],
            "-vf", "crop=ih*(9/16):ih",
            "-c:a", "copy",
            output_clip
        ]
        subprocess.run(crop_cmd)
        print(f"--- Бэлэн боллоо: {output_clip} ---")

if __name__ == "__main__":
    process_streamers()
