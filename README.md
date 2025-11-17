# Data Downloader
Un script en Python para descargar datos de forma sencilla.

<div align="center">

# Data_Downloader
### El convertidor y descargador MÁS POTENTE para Termux

![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-success.svg?style=for-the-badge)

**Descarga, mejora y convierte videos, audios e imágenes con calidad profesional — TODO desde tu celular.**

Creado por **Shadow-TermDev** — El lord de Termux

</div>

## Características ÉPICAS

- Descarga de TikTok, Instagram, YouTube, Facebook (sin marca de agua)  
- Mejorador de video (720p → 4K), audio (voz cristalina + graves profundos) e imágenes
- Convertidor profesional:
  → Video → Audio
  → Audio → MP3 / FLAC / M4A / OGG / WAV
  → Imagen → PNG / WEBP / JPG / GIF / ICO
- Progreso en tiempo real (beta)
- Interfaz hermosa con colorama + rich
- 100% funcional en Termux Android

## Instalación (30 segundos)

```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg git -y

git clone https://github.com/Shadow-TermDev/Data_Downloader.git
cd Data_Downloader

pip install -r requirements.txt
python main.py
