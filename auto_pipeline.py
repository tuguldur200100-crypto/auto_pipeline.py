import os
import subprocess

# Стримерүүдийн жагсаалт (Энд өөрийн хүссэн стримерийн YouTube линкийг тавина)
STREAMERS = [
    {"name": "Streamer1", "url": "https://www.youtube.com/watch?v=EXAMPLE_1"},
]

def process_and_upload():
    for streamer in STREAMERS:
        print(f"--- Processing {streamer['name']} ---")
        output_file = f"{streamer['name']}_clip.mp4"
        
        # yt-dlp ашиглан бичлэгээс хэсэг татаж авах
        download_cmd = [
            "yt-dlp",
            "-f", "mp4",
            "--external-downloader", "ffmpeg",
            "--external-downloader-args", "ffmpeg_i:-ss 00:10:00 -t 45",
            streamer["url"],
            "-o", "raw_temp.mp4",
            "--force-overwrites"
        ]
        
        try:
            subprocess.run(download_cmd, check=True)
            
            # 9:16 Босоо формат руу шилжүүлэх (FFmpeg crop)
            crop_cmd = [
                "ffmpeg", "-y",
                "-i", "raw_temp.mp4",
                "-vf", "crop=ih*(9/16):ih",
                "-c:a", "copy",
                output_file
            ]
            subprocess.run(crop_cmd, check=True)
            print(f"Clip for {streamer['name']} is ready: {output_file}")
            
        except Exception as e:
            print(f"Aldaa garlaa: {e}")

if __name__ == "__main__":
    process_and_upload()
