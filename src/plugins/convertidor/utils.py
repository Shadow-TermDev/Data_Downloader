import subprocess
from colorama import Fore, Style

def ejecutar_comando(comando, salida):
    """Ejecuta un comando en la terminal y maneja errores."""
    try:
        resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(Fore.GREEN + f"✅ Conversión completada: {salida}" + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"❌ La conversión falló. Verifica el archivo y el formato." + Style.RESET_ALL)
        print(Fore.YELLOW + f"🔍 Error detallado: {e.stderr}" + Style.RESET_ALL)

