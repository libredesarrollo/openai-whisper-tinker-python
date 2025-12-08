pyinstaller --onefile --windowed --add-data "venv/Lib/site-packages/customtkinter;customtkinter" transcriptor_app.py

https://gemini.google.com/app/dc2cf3e6543e634f?hl=es



$ pip install -U openai-whisper.


cd C:\Users\andre\Desktop\proy\python\venv

whisper "ruta/a/MiVideoDeVimeo.mp4" --language es

.\Scripts\activate

Reemplaza "ruta/a/MiVideoDeVimeo.mp4" con la ubicación real de tu archivo.

El parámetro --language es indica que el audio está en español.


🛠️ Instalación de OpenAI Whisper (Versión Oficial de GitHub)
Sigue estos pasos para instalar y usar Whisper en tu computadora. Este método garantiza un procesamiento local (offline) y es gratuito.

1. Requisitos Previos
Necesitas tener instalados dos elementos clave:

Python: La versión 3.8 o superior.

FFmpeg: Esta es una biblioteca esencial para que Whisper pueda abrir archivos de video (como el .mp4 que descargaste de Vimeo) y extraer el audio.

Instalación de FFmpeg
Windows: Este es el paso más complejo en Windows. La forma más fácil es usar un gestor de paquetes como Chocolatey (choco install ffmpeg). Si no usas Chocolatey, debes descargar el paquete binario de FFmpeg y añadir la ruta a la carpeta bin a tu variable de entorno PATH de Windows.

macOS (Usando Homebrew): Abre tu Terminal y ejecuta:

Bash

brew install ffmpeg
Linux (Debian/Ubuntu): Abre tu Terminal y ejecuta:

Bash

sudo apt update && sudo apt install ffmpeg
2. Instalación del Paquete Whisper
Una vez que tengas Python y FFmpeg listos, instala Whisper a través del gestor de paquetes pip:

Abre tu Terminal, Símbolo del Sistema o PowerShell.

Ejecuta el siguiente comando:

Bash

pip install -U openai-whisper
(Si tienes problemas, puedes intentar: pip install -U git+https://github.com/openai/whisper.git)





¡Excelente! Si estás usando Windows, los pasos para instalar la versión oficial de OpenAI Whisper requieren un poco más de detalle, especialmente con la instalación de FFmpeg.

Aquí está la guía paso a paso para la instalación gratuita y local en Windows:

💻 Instalación de Whisper en Windows
Paso 1: Instalar Python
Whisper está basado en Python, así que es fundamental tenerlo instalado.

Descargar Python: Ve al sitio web oficial de Python: https://www.python.org/downloads/windows/ y descarga la última versión para Windows.

Ejecutar el Instalador:

MUY IMPORTANTE: Al iniciar la instalación, asegúrate de marcar la casilla que dice "Add python.exe to PATH" (Añadir python.exe a PATH) en la primera pantalla. Esto te ahorrará muchos problemas más adelante.

Haz clic en "Install Now" y espera a que termine.

Paso 2: Instalar FFmpeg
FFmpeg es necesario para que Whisper pueda extraer el audio de los archivos de video (.mp4, .mov, etc.) de Vimeo.

La forma más sencilla y recomendada para Windows es usando Chocolatey (un gestor de paquetes de Windows) o la instalación manual:

Opción A: Usar Chocolatey (Recomendado)
Instalar Chocolatey:

Abre el menú de inicio y busca PowerShell. Haz clic derecho y selecciona "Ejecutar como administrador".

Pega y ejecuta el siguiente comando:

Bash

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
Instalar FFmpeg: Cierra y vuelve a abrir PowerShell como administrador. Ejecuta:

Bash

choco install ffmpeg