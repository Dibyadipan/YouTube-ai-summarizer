# 🎯 YouTube Summarizer & Note Taker (Local AI-Powered)

A complete pipeline that:
1. Downloads audio from a YouTube video
2. Transcribes it using OpenAI Whisper (tiny model)
3. Summarizes the transcript using **Ollama’s local LLaMA3 model**
4. Saves the summary as a well-formatted `.txt` file

> ✅ No paid APIs. No cloud dependencies. Fully local and privacy-preserving.

---

## 🚀 Features

- ✅ YouTube audio download using `yt-dlp`
- ✅ Audio transcription using `whisper` (OpenAI)
- ✅ Summarization via `ollama run llama3` (local LLM)
- ✅ Output saved as a plain text file
- ✅ Logs all steps for transparency & debugging
- 🔜 (Optional) Push notes to Notion subpages with `notion-client`

---

## 🧠 Tech Stack

| Component          | Description                                |
|-------------------|--------------------------------------------|
| `yt-dlp`          | Downloads best-quality YouTube audio       |
| `ffmpeg`          | Extracts audio in `.mp3` format            |
| `whisper`         | Transcribes speech to text                 |
| `ollama` + `llama3` | Local LLM used for text summarization     |
| `Python` + `dotenv`| Manages orchestration and env configs     |
| `notion-client` (optional) | Pushes notes to Notion (via API)  |

---

## 📦 Installation Guide

### 1. Clone the repository and install dependencies

```bash
git clone https://github.com/your-username/youtube-summarizer-local.git
cd youtube-summarizer-local
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Note: Install and set up Ollama
https://ollama.com/download
```bash
ollama run llama3
```
# This will auto-download and spin up the local LLaMA3 model. Keep it ready before running the script.

### 🔑 .env Configuration
If you want to use Notion (optional), create a .env file like:
NOTION_API_KEY=your_secret_key
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxx
Otherwise, it defaults to writing summaries to summary_output.txt.



### ⚠️ Known Limitations
Uses Whisper tiny model for speed – may affect accuracy for long videos

Local Ollama summarization depends on system RAM (~8GB recommended)

Currently pushes to plain text file — Notion support is optional


### 📌 Why I Built This
I wanted a free, local, AI-powered system to:

Summarize long cybersecurity videos

Store key takeaways into my Notion knowledge base

Avoid OpenAI API costs while learning smarter


### 🧠 Credits
Ollama
Whisper by OpenAI
yt-dlp
Notion SDK for Python

### 🤝 Contributions
Feel free to fork, tweak, and suggest improvements via PRs.
Ideas: add keyword tagging, voice summarization, or integrate into a Notion database.

### 📬 Contact
Built by @Dibyadipan
www.linkedin.com/in/dibyadipan


