<div align="center">

# 🎬 Data Downloader

### **La herramienta definitiva para descargar, convertir y mejorar multimedia en Termux**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.6.0-success.svg?style=for-the-badge)

**Descarga, mejora y convierte videos, audios e imágenes — TODO desde tu celular.**

[🌐 Sitio Web](https://Shadow-TermDev.github.io) • [🐛 Reportar Bug](https://github.com/Shadow-TermDev/Data_Downloader/issues) • [✨ Solicitar Feature](https://github.com/Shadow-TermDev/Data_Downloader/issues)

---

## 🌟 Características

### 📥 Descargador
- ✅ Videos de YouTube, TikTok, Instagram y más
- ✅ Audio en alta calidad (hasta 320kbps)
- ✅ Imágenes con resolución original
- ✅ Sin marcas de agua
- ✅ Metadatos y portadas incluidos
- ✅ Soporte para PO Token (anti-bot)
- ✅ Interfaz mejorada y más limpia

### 🔄 Convertidor
- ✅ **Video:** MP4, MKV, AVI, MOV, WebM
- ✅ **Audio:** MP3, WAV, AAC, FLAC, OGG, M4A
- ✅ **Imagen:** PNG, JPG, WebP, BMP, GIF
- ✅ Extracción de audio desde video
- ✅ Preservación de metadatos

### ⬆️ Mejorador de Calidad
- ✅ Upscaling de video hasta 4K
- ✅ Mejora de bitrate de audio
- ✅ Aumento de resolución de imágenes
- ✅ Filtros de nitidez y contraste

---

## 🚀 Instalación Rápida

### Requisitos Previos
- Android 7.0+
- Termux desde [F-Droid](https://f-droid.org/packages/com.termux/)

### 📱 Instalación Paso a Paso

1. **Abre Termux y ejecuta:**

   ```bash
   termux-setup-storage
   ```

2. **Actualiza paquetes e instala dependencias:**

   ```bash
   pkg update -y && pkg upgrade -y
   pkg install python ffmpeg git -y
   ```

3. **Clona el repositorio e instala:**

   ```bash
   git clone https://github.com/Shadow-TermDev/Data_Downloader.git
   cd Data_Downloader
   pip install -r requirements.txt
   ```

4. **Ejecuta el programa:**

   ```bash
   python src/main.py
   ```
   
   O usa el script de inicio:
   ```bash
   chmod +x start && ./start
   ```

---

## 📖 Uso

Una vez ejecutado el programa, puedes descargar audios y videos usando el enlace correspondiente. Sigue las instrucciones en pantalla para seleccionar el formato y la calidad deseada.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

</div>
