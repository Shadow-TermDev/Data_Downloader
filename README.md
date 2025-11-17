<div align="center">

# Data_Downloader
### El convertidor y descargador MÁS POTENTE para Termux

![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.4-success.svg?style=for-the-badge)

**Descarga, mejora y convierte videos, audios e imágenes con calidad profesional — TODO desde tu celular.**

**Creado por Shadow-TermDev — El Lord de Termux Perú**

</div>

## Características ÉPICAS

- Descarga sin marca de agua: TikTok, Instagram, YouTube, Facebook  
- Mejorador de video (720p → 4K), audio (voz cristalina + graves profundos) e imágenes  
- Convertidor profesional:  

  → Video → Audio (con portada)  
  
  → Audio → MP3 / FLAC / M4A / OGG / WAV (con portada)  
  
  → Imagen → PNG / WEBP / JPG / GIF / ICO  
  
- Progreso en tiempo real  
- Interfaz hermosa con colorama + rich  
- 100% funcional en Termux Android  

## Instalación ULTRA FÁCIL (3 pasos)

### 1. Instala Termux (si aún no lo tienes)

[![Descargar Termux desde F-Droid](https://img.shields.io/badge/Download-Termux%20(F--Droid)-25A362?style=for-the-badge&logo=f-droid)](https://f-droid.org/packages/com.termux/)
[![Descargar F-Droid](https://img.shields.io/badge/Download-F--Droid-3D7AB9?style=for-the-badge&logo=f-droid)](https://f-droid.org/F-Droid.apk)

> Abre Termux por primera vez y acepta los permisos de almacenamiento

### 2. Instala Data_Downloader

```bash
pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && \
git clone https://github.com/Shadow-TermDev/Data_Downloader.git && \
cd Data_Downloader && \
pip install -r requirements.txt && \
python main.py
