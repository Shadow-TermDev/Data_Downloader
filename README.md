<div align="center">

# 🎬 Data Downloader

### **The ultimate toolkit to download, convert and enhance media on Termux**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.8.3-success.svg?style=for-the-badge)

**Download, enhance and convert videos, audios and images — ALL from your phone.**

[🌐 Website](https://Shadow-TermDev.github.io) • [🐛 Report Bug](https://github.com/Shadow-TermDev/Data_Downloader/issues) • [✨ Request Feature](https://github.com/Shadow-TermDev/Data_Downloader/issues)

---

## 🌟 Features

### 📥 Downloader
- ✅ Videos from YouTube, TikTok, Instagram and more
- ✅ High-quality audio (up to 320kbps)
- ✅ Images at original resolution
- ✅ No watermarks
- ✅ Metadata and covers included
- ✅ PO Token support (anti-bot)
- ✅ Clean, improved interface with navigable arrow-key TUI (no extra dependencies)
- ✅ 🔎 YouTube search (search & download without leaving the app)

### 🔄 Converter
- ✅ **Video:** MP4, MKV, AVI, MOV, WebM
- ✅ **Audio:** MP3, WAV, AAC, FLAC, OGG, M4A
- ✅ **Image:** PNG, JPG, WebP, BMP, GIF
- ✅ Audio extraction from video
- ✅ Metadata preservation

### ⬆️ Quality Enhancer
- ✅ Video upscaling up to 4K
- ✅ Audio bitrate boost
- ✅ Image resolution boost
- ✅ Sharpness and contrast filters

---

## 🚀 Quick Install

### Prerequisites
- Android 7.0+
- Termux from [F-Droid](https://f-droid.org/packages/com.termux/)

### 📱 Step-by-step Install

1. **Open Termux and run:**

   ```bash
   termux-setup-storage
   ```

2. **Update packages and install dependencies:**

   ```bash
   pkg update -y && pkg upgrade -y
   pkg install python ffmpeg git -y
   ```

3. **Clone the repo and install:**

   ```bash
   git clone https://github.com/Shadow-TermDev/Data_Downloader.git
   cd Data_Downloader
   pip install -r requirements.txt
   ```

4. **Run the app:**

   ```bash
   python src/main.py
   ```
   
   Or use the launcher script:
   ```bash
   chmod +x start && ./start
   ```

---

## 📖 Usage

Once the app is running, navigate with ↑/↓ + Enter (or 1-6 quick pick, q to go back). You can download audios and videos with the matching link, or press **Search YouTube** to search first and download straight away.

### 📥 Output directories

Files are auto-saved into organized folders:

| Type      | Directory                                        |
|-----------|--------------------------------------------------|
| 🎬 Video  | `/storage/emulated/0/Movies/Videos_Downloader`   |
| 🎵 Audio  | `/storage/emulated/0/Music/Music_Downloader`     |
| 🖼️ Image  | `/storage/emulated/0/Pictures/Picture_Downloader`|

> The converter and enhancer save processed files next to the original with `_converted`, `_audio`, `_enhanced` suffixes.

### ⚠️ Troubleshooting

- **YouTube blocks downloads** ("Sign in to confirm"): install the PO Token provider with `pip install bgutil-ytdlp-pot-provider` or use a VPN.
- **TikTok / Facebook ask for cookies** (403 error): export your browser cookies with `yt-dlp --cookies-from-browser chrome URL`.
- **Keep yt-dlp updated** to avoid platform breakage: `pip install -U yt-dlp`.
- **FFmpeg is required** for conversions, enhancements and cover embedding: `pkg install ffmpeg`.

---

## 📄 License

This project is under the MIT license. See [LICENSE](LICENSE) for details.

</div>
