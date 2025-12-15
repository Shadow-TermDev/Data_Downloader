<div align="center">

<<<<<<< HEAD
# Data_Downloader
### Una buena opción si quieres sencillez y rapidez 
=======
# 🎬 Data Downloader
>>>>>>> f99237d (New changes)

### **La herramienta definitiva para descargar, convertir y mejorar multimedia en Termux**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Android-green.svg?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.4.2-success.svg?style=for-the-badge)

**Descarga, mejora y convierte videos, audios e imágenes — TODO desde tu celular.**

[🌐 Sitio Web](https://Shadow-TermDev.github.io) • [📖 Documentación](./docs) • [🐛 Reportar Bug](https://github.com/Shadow-TermDev/Data_Downloader/issues) • [✨ Solicitar Feature](https://github.com/Shadow-TermDev/Data_Downloader/issues)

<<<<<<< HEAD
## Características del PROYECTO

- Descarga videos sin marca de agua
- Descarga música
- Convierte tus archivos a los formatos que desees 
=======
---
>>>>>>> f99237d (New changes)

</div>

## 🌟 Características

### 📥 Descargador
- ✅ Videos de YouTube, TikTok, Instagram y más
- ✅ Audio en alta calidad (hasta 320kbps)
- ✅ Imágenes con resolución original
- ✅ Sin marcas de agua
- ✅ Metadatos y portadas incluidos

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

<a href="https://f-droid.org/packages/com.termux/" target="_blank">
  <img src="https://img.shields.io/badge/Download-Termux%20(F--Droid)-25A362?style=for-the-badge&logo=f-droid" alt="Termux F-Droid"/>
</a>

#### 1. Configurar Termux

<<<<<<< HEAD
### 2. Abre Termux y ejecuta los siguientes comandos uno por uno

- Dale permisos de almacenamiento a Termux
```text
=======
```bash
# Dar permisos de almacenamiento
>>>>>>> f99237d (New changes)
termux-setup-storage

<<<<<<< HEAD
- Actualiza los paquetes
```text
=======
# Actualizar paquetes
>>>>>>> f99237d (New changes)
pkg update -y && pkg upgrade -y

<<<<<<< HEAD
- Instala los recursos necesarios para clonar el repositorio
```text
pkg install python ffmpeg git -y
```

- Clona el repositorio
```text
=======
# Instalar dependencias del sistema
pkg install python ffmpeg git -y
```

#### 2. Instalar Data Downloader

```bash
# Clonar el repositorio
>>>>>>> f99237d (New changes)
git clone https://github.com/Shadow-TermDev/Data_Downloader.git

# Entrar al directorio
cd Data_Downloader

# Instalar dependencias de Python
pip install -r requirements.txt

# Ejecutar el programa
python src/main.py
```

<<<<<<< HEAD
- Entra a la carpeta del proyecto
```text
=======
---

## 📖 Uso

### Ejecución

```bash
>>>>>>> f99237d (New changes)
cd Data_Downloader
python src/main.py
```

<<<<<<< HEAD
- Instala los requerimientos de python
```text
pip install -r requirements.txt
```

- Ejecuta el programa y disfruta!!!!
```text
python main.py
=======
### Ejemplos Rápidos

#### Descargar un video de YouTube
```
1. Selecciona "Descargar contenido" (opción 1)
2. Elige "Descargar video" (opción 1)
3. Pega la URL del video
4. Selecciona la calidad deseada
```

#### Convertir video a MP3
>>>>>>> f99237d (New changes)
```
1. Selecciona "Convertir archivos" (opción 2)
2. Elige "Video → Audio" (opción 2)
3. Ingresa el nombre del video
4. Selecciona "mp3" como formato
```

#### Mejorar calidad de imagen
```
1. Selecciona "Mejorar calidad" (opción 3)
2. Elige "Mejorar imagen" (opción 3)
3. Ingresa el nombre de la imagen
4. Selecciona el nivel de mejora
```

---

## 📂 Estructura del Proyecto

```
Data_Downloader/
├── src/
│   ├── main.py              # Punto de entrada
│   ├── downloader/          # Módulo de descarga
│   ├── converter/           # Módulo de conversión
│   ├── enhancer/            # Módulo de mejora
│   └── utils/               # Utilidades
├── config/                  # Configuración
├── docs/                    # Documentación
└── assets/                  # Recursos
```

---

## 🛠️ Tecnologías Utilizadas

| Librería | Uso |
|----------|-----|
| **yt-dlp** | Descarga de videos/audio |
| **FFmpeg** | Procesamiento multimedia |
| **Pillow** | Procesamiento de imágenes |
| **colorama** | Interfaz colorida |
| **pyfiglet** | Arte ASCII |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](./docs/CONTRIBUTING.md) para más detalles.

### Proceso de Contribución

1. **Fork** el proyecto
2. Crea tu **rama de feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

---

## 📝 Changelog

### v1.4.2 (Actual)
- ✨ Mejora en la detección de calidades
- 🐛 Fix en conversión de audio con portada
- 📦 Optimización de descarga de imágenes

### v1.4.0
- ✨ Soporte para TikTok HD
- ✨ Mejora de calidad de imágenes con upscaling
- 🔄 Refactorización del sistema de menús

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

<div align="center">

**Shadow-TermDev**

*El Lord de Termux*

[![Website](https://img.shields.io/badge/Website-Shadow--TermDev.github.io-blue?style=for-the-badge&logo=google-chrome)](https://Shadow-TermDev.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-Shadow--TermDev-black?style=for-the-badge&logo=github)](https://github.com/Shadow-TermDev)

</div>

---

## ⭐ Apóyame

Si este proyecto te ha sido útil, considera darle una ⭐ en GitHub.

¡Tu apoyo es muy apreciado! 🙏

---

## 📞 Soporte

¿Necesitas ayuda? 

- 📧 Abre un [Issue](https://github.com/Shadow-TermDev/Data_Downloader/issues)
- 💬 Revisa la [Documentación](./docs)
- 🌐 Visita mi [Sitio Web](https://Shadow-TermDev.github.io)

---

<div align="center">

**Hecho con ❤️ por Shadow-TermDev**

*Descarga inteligente, conversión rápida, mejora profesional*

</div>
