import os
import subprocess
import yt_dlp
from dotenv import load_dotenv
import whisper
# from notion_client import Client
from datetime import datetime

# # Load .env values
# load_dotenv()
# NOTION_API_KEY = os.getenv("NOTION_API_KEY")
# NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID") 

# Logging setup
def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# Step 1: Download Audio
def download_audio(video_url):
    # Create downloads dir if it doesn't exist
    os.makedirs("downloads", exist_ok=True)

    output_path = os.path.join("downloads", "audio.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get('title', 'Untitled')
        
        audio_file = os.path.join("downloads", "audio.mp3")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"{audio_file} not found after download.")

        return audio_file, title
    except Exception as e:
        log(f"Error in download_audio: {e}")
        raise

# Step 2: Transcribe Audio
def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"{audio_path} not found")
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        log("Transcription complete!")
        return result["text"]
    except Exception as e:
        log(f"Error in transcribe_audio: {e}")
        raise

# Step 3: Summarize via Ollama
def summarize_text(text):
    try:
        prompt = f"Summarize the following transcript into structured technical notes relevant to cybersecurity:\n\n{text}"
        result = subprocess.run(
            ['ollama', 'run', 'llama3'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=180
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        log("Summarization successful!")
        return result.stdout.strip()
    except Exception as e:
        log(f"Error in summarize_text: {e}")
        raise

# Step 4: Save to Notion as a Subpage
# def create_subpage(title, summary, url):
#     try:
#         notion = Client(auth=NOTION_API_KEY)

#         chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]
#         children_blocks = [
#             {
#                 "object": "block",
#                 "type": "paragraph",
#                 "paragraph": {
#                     "rich_text": [{"type": "text", "text": {"content": chunk}}]
#                 }
#             }
#             for chunk in chunks
#         ]

#         # Add link and metadata as header
#         children_blocks.insert(0, {
#             "object": "block",
#             "type": "heading_3",
#             "heading_3": {
#                 "rich_text": [{"type": "text", "text": {"content": f"YouTube Link: {url}"}}]
#             }
#         })

#         response = notion.pages.create(
#             parent={"page_id": NOTION_PARENT_PAGE_ID},
#             properties={
#                 "title": {
#                     "title": [{"type": "text", "text": {"content": title}}]
#                 }
#             },
#             children=children_blocks
#         )
#         log(f"✅ Subpage created for: {title}")
#         return response
#     except Exception as e:
#         log(f"Error in create_subpage: {e}")
#         raise

# Cleanup temp files
def cleanup(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            log(f"Deleted temporary file: {file_path}")
    except Exception as e:
        log(f"Cleanup failed for {file_path}: {e}")

# Orchestrator
def run_agent(youtube_url):
    log("\n=== Agent Run Started ===")
    try:
        log("[1] Downloading audio...")
        audio_file, title = download_audio(youtube_url)

        log("[2] Transcribing...")
        transcript = transcribe_audio(audio_file)

        log("[3] Summarizing with Ollama...")
        summary = summarize_text(transcript)

        # log("[4] Creating Notion subpage...")
        # create_subpage(title, summary, youtube_url)
        
        log("[4] Writing summary to file...")
        with open("summary_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n\n")
            f.write(summary)
            log("Summary written to summary_output.txt")
        
        log("Agent completed successfully!!!")
    except Exception as e:
        log(f"Agent failed: {e}")
    finally:
        cleanup("audio.mp3")
        log("=== Agent Run Finished ===\n")

if __name__ == "__main__":
    url = input("Enter YouTube video link: ")
    os.makedirs("downloads", exist_ok=True)
    run_agent(url)
