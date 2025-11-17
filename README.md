<div align="center">

# Data_Downloader
### El convertidor y descargador MÁS POTENTE para Termux

![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.4-success.svg?style=for-the-badge)

**Descarga, mejora y convierte videos, audios e imágenes con calidad profesional — TODO desde tu celular.**

**Creado por Shadow-TermDev — El Lord de Termux**

## Características del PROYECTO

- Descarga sin marca de agua: TikTok, Instagram, YouTube, Facebook  
- Mejorador de video (720p → 4K), audio (voz cristalina + graves profundos) e imágenes  
- Convertidor profesional:  

  → Video → Audio (con portada)  
  
  → Audio → MP3 / FLAC / M4A / OGG / WAV (con portada)  
  
  → Imagen → PNG / WEBP / JPG / GIF / ICO  
  
- Progreso en tiempo real  
- Interfaz hermosa con colorama + rich  
- 100% funcional en Termux Android  

</div>

### 1. Instala Termux si no lo tienes desde F-Droid (versión oficial)

<a href="https://f-droid.org/packages/com.termux/" target="_blank">
  <img src="https://img.shields.io/badge/Download-Termux%20(F--Droid)-25A362?style=for-the-badge&logo=f-droid" alt="Termux F-Droid"/>
</a>

<a href="https://f-droid.org/F-Droid.apk" target="_blank">
  <img src="https://img.shields.io/badge/Download-F--Droid-3D7AB9?style=for-the-badge&logo=f-droid" alt="F-Droid APK"/>
</a>

### 2. Abre Termux y ejecuta los siguientes comandos uno por uno

## Dale permisos de almacenamiento a Termux
```bash
termux-setup-storage
```

## Actualiza los repositorios y paquetes
```bash
pkg update -y && pkg upgrade -y
```

## Instala los recursos necesarios para clonar el proyecto
```bash
pkg install python ffmpeg git -y
```

## Clona el proyecto o repositorio
```bash
git clone https://github.com/Shadow-TermDev/Data_Downloader.git
```

## Entra a la carpeta del proyecto

```bash
cd Data_Downloader
```

## Instala los requerimientos de python
```bash
pip install -r requirements.txt
```

## Ejecuta el programa y disfruta!!!!
```bash
python main.py
```
