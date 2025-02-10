import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import http.server
import os
import psutil
import re
import psutil
import time
import requests
import sys

# Variables globales
server_process = None
cloudflare_process = None
selected_directory = os.path.expanduser("~")  # Carpeta inicial (Usuario actual)
tunnel_url = ""

# Detectar la ubicación del ejecutable o script
if getattr(sys, 'frozen', False):
    # Si está en modo ejecutable (PyInstaller)
    base_path = sys._MEIPASS
else:
    # Si está en modo script (Python normal)
    base_path = os.path.dirname(os.path.abspath(__file__))

ICON_PATH = os.path.join(base_path, "icono.ico")

# Detectar la ubicación del ejecutable en tiempo de ejecución
if getattr(sys, 'frozen', False):
    # Si está en modo ejecutable (PyInstaller)
    base_path = os.path.dirname(sys.executable)
else:
    # Si está en modo script (Python normal)
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ruta donde se descargará cloudflared.exe
cloudflared_path = os.path.join(base_path, "cloudflared.exe")

# URL de descarga de Cloudflare Tunnel
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Manejador personalizado para registrar y mostrar cada acceso en los logs."""
    
    def log_message(self, format, *args):
        """Registra cada acceso en los logs sin eliminar registros anteriores."""
        path = self.path
        client_ip = self.client_address[0]

        # Evitar registrar favicon.ico (solicitud automática de los navegadores)
        if path != "/favicon.ico":
            log_message(f"Acceso detectado: {client_ip} - {path}")

def delete_cloudflared():
    """Elimina el archivo cloudflared.exe si existe."""
    if os.path.exists(cloudflared_path):
        try:
            os.remove(cloudflared_path)
            log_message("Cloudflare Tunnel ha sido eliminado correctamente.")
            messagebox.showinfo("Eliminado", "Cloudflare Tunnel ha sido eliminado correctamente.")
        except Exception as e:
            log_message(f"Error al eliminar Cloudflare Tunnel: {str(e)}")
            messagebox.showerror("Error", f"No se pudo eliminar Cloudflare Tunnel: {str(e)}")
    else:
        log_message("Cloudflare Tunnel no está presente en el sistema.")
        messagebox.showwarning("No encontrado", "El archivo de Cloudflare Tunnel no existe.")


def copy_link():
    if tunnel_url:
        root.clipboard_clear()
        root.clipboard_append(tunnel_url)
        root.update()
        messagebox.showinfo("Copiado", "El enlace se ha copiado al portapapeles.")

def is_port_in_use(port):
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            return True
    return False

def stop_all():
    """Ejecuta la limpieza en un hilo separado para evitar que la GUI se congele."""
    threading.Thread(target=stop_all_thread, daemon=True).start()

def stop_all_thread():
    """Detiene el servidor HTTP y el túnel de Cloudflare de la forma más simple posible."""
    global server_process, cloudflare_process

    log_message("Deteniendo procesos del servidor y Cloudflare Tunnel...")

    # Cerrar servidor HTTP correctamente
    if server_process:
        log_message("Deteniendo servidor HTTP...")
        try:
            requests.get("http://localhost:9876")  # Intenta hacer una solicitud para cerrarlo
        except requests.exceptions.RequestException:
            pass  # Puede fallar si ya está cerrado

        server_process.terminate()  # Simular Ctrl + C para detener el servidor
        server_process.wait()  # Esperar a que el proceso termine
        server_process = None  # Marcarlo como detenido
        log_message("Servidor HTTP detenido correctamente.")

    # Cerrar Cloudflare Tunnel (cloudflared.exe)
    log_message("Cerrando túnel de Cloudflare...")
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        if "cloudflared" in proc.info["name"].lower():
            log_message(f"Matando proceso Cloudflare Tunnel (PID {proc.info['pid']})...")
            proc.terminate()
            time.sleep(1)
            if proc.is_running():
                proc.kill()  # Si sigue vivo, lo mata forzadamente

    log_message("Servidor HTTP y túnel Cloudflare detenidos correctamente.")
    messagebox.showinfo("Detenido", "El servidor HTTP y el túnel de Cloudflare han sido cerrados correctamente.")



def select_directory():
    global selected_directory
    directory = filedialog.askdirectory(initialdir=selected_directory, title="Selecciona la carpeta a compartir")
    if directory:
        selected_directory = directory
        dir_label.config(text=f"Carpeta seleccionada: {directory}")
        log_message(f"Se ha seleccionado la carpeta: {directory}")

def log_message(message):
    """Muestra mensajes en la interfaz gráfica."""
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.yview(tk.END)
    status_text.config(state=tk.DISABLED)

def download_cloudflared():
    if os.path.exists(cloudflared_path):
        log_message("Cloudflare Tunnel ya está descargado.")
        return
    threading.Thread(target=download_cloudflared_thread, daemon=True).start()

def download_cloudflared_thread():
    log_message("Descargando Cloudflare Tunnel...\n")
    try:
        response = requests.get(CLOUDFLARED_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        bar_length = 40
        if response.status_code == 200:
            with open(cloudflared_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size)
                        filled_length = int(bar_length * progress)
                        bar = "█" * filled_length + "." * (bar_length - filled_length)
                        status_text.config(state=tk.NORMAL)
                        status_text.delete("end-2l", "end-1c")
                        status_text.insert(tk.END, f"Progreso: [{bar}] {int(progress * 100)}%\n")
                        status_text.yview(tk.END)
                        status_text.config(state=tk.DISABLED)
            log_message("\nDescarga completa: Cloudflare Tunnel actualizado.")
            messagebox.showinfo("Descarga completa", "Cloudflare Tunnel se ha descargado correctamente.")
        else:
            log_message("Error al descargar Cloudflare Tunnel.")
            messagebox.showerror("Error", "No se pudo descargar Cloudflare Tunnel.")
    except Exception as e:
        log_message(f"Error en la descarga: {str(e)}")
        messagebox.showerror("Error", f"No se pudo descargar Cloudflare Tunnel: {str(e)}")

def start_server():
    """Inicia el servidor HTTP sin abrir una consola."""
    global server_process

    if server_process:
        messagebox.showwarning("Servidor en ejecución", "El servidor ya está activo.")
        return

    if is_port_in_use(9876):
        messagebox.showerror("Error", "El puerto 9876 ya está en uso. Detén el proceso y vuelve a intentarlo.")
        return

    os.chdir(selected_directory)
    log_message("Iniciando servidor HTTP...")

    try:
        # ✅ Se añade `creationflags=subprocess.CREATE_NO_WINDOW` para evitar que se abra la consola
        server_process = subprocess.Popen(
            ["python", "-m", "http.server", "9876", "--bind", "0.0.0.0"],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # 🚀 Evita la consola emergente
        )

        log_message("Servidor HTTP iniciado en el puerto 9876.")

        # Hilo que captura la salida del servidor HTTP y la muestra en los logs
        def monitor_server_output():
            for line in iter(server_process.stdout.readline, ''):
                log_message(f"Servidor HTTP: {line.strip()}")

        threading.Thread(target=monitor_server_output, daemon=True).start()

    except Exception as e:
        log_message(f"Error al iniciar el servidor HTTP: {str(e)}")
        messagebox.showerror("Error", f"No se pudo iniciar el servidor HTTP: {str(e)}")




def start_tunnel():
    """Inicia Cloudflare Tunnel sin mostrar consola."""
    global cloudflare_process, tunnel_url

    if cloudflare_process:
        messagebox.showwarning("Túnel en ejecución", "El túnel ya está activo.")
        return

    if not os.path.exists(cloudflared_path):
        messagebox.showerror("Error", "Cloudflare Tunnel no está instalado. Descárgalo primero.")
        return

    log_message("Iniciando túnel Cloudflare...")

    def run_cloudflare():
        global tunnel_url
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", "http://localhost:9876"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        for line in iter(process.stdout.readline, ""):
            if "https://" in line:
                match = re.search(r'https://[a-zA-Z0-9.-]+\.trycloudflare\.com', line)
                if match:
                    tunnel_url = match.group(0)
                    log_message(f"TÚNEL ACTIVO, ENLACE:\n\n{tunnel_url}")

                    link_button.config(state=tk.NORMAL)
                    break

    cloudflare_thread = threading.Thread(target=run_cloudflare, daemon=True)
    cloudflare_thread.start()
    cloudflare_process = cloudflare_thread


def show_instructions():
    """Muestra las instrucciones en una ventana independiente sin bloquear la principal."""
    instructions_window = tk.Toplevel(root)  # ✅ Crea una ventana secundaria
    instructions_window.title("ℹ️ Cómo Usar")
    instructions_window.geometry("900x400")
    instructions_window.resizable(False, False)  # No permitir redimensionar
    instructions_window.iconbitmap(ICON_PATH)  # ✅ Aplica el icono también a la ventana secundaria

    # Texto con las instrucciones
    instrucciones = """\
📌 MANUAL DE INSTRUCCIONES

1. SELECCIONAR CARPETA A COMPARTIR
-----------------------------------------
- Haz clic en "Seleccionar Carpeta".
- Aparecerá un explorador de archivos.
- Selecciona la carpeta que contiene los archivos que deseas compartir.
- La ruta de la carpeta seleccionada se mostrará en la interfaz.

2. INICIAR EL SERVIDOR HTTP
-----------------------------------------
- Haz clic en "Iniciar Servidor HTTP".
- Esto activará un servidor local en el puerto 9876.
- Este servidor permitirá compartir los archivos en la red local.

3. DESCARGAR CLOUDFLARE TUNNEL (si no lo tienes)
-----------------------------------------
- Haz clic en "Descargar Cloudflare Tunnel".
- Si es la primera vez que usas el programa, necesitas descargar cloudflared.exe.
- Espera a que la descarga finalice antes de continuar.
- Si ya lo descargaste antes, puedes omitir este paso.

4. INICIAR CLOUDFLARE TUNNEL
-----------------------------------------
- Haz clic en "Iniciar Cloudflare Tunnel".
- Esto creará un túnel seguro con Cloudflare y generará un enlace público.
- Cuando el túnel esté activo, el enlace aparecerá en la interfaz.
- El enlace se copiará automáticamente al portapapeles.

5. COMPARTIR EL ENLACE
-----------------------------------------
- Si necesitas copiar nuevamente el enlace, haz clic en "Copiar Enlace".
- Comparte el enlace con las personas que necesiten acceder a tus archivos.
- Los usuarios podrán ver y descargar los archivos sin configuraciones adicionales.

6. DETENER TODO
-----------------------------------------
- Haz clic en "Detener Todo" cuando termines de compartir los archivos.
- Esto cerrará tanto el servidor HTTP como el túnel de Cloudflare.
- Es recomendable hacer esto para liberar recursos y evitar accesos no autorizados.

7. BORRAR CLOUDFLARE TUNNEL
-----------------------------------------
- Si deseas eliminar cloudflared.exe de tu sistema, haz clic en "Eliminar Cloudflare Tunnel".
- Esto eliminará el archivo descargado, pero podrás volver a descargarlo más adelante si lo necesitas.

📌 NOTAS IMPORTANTES
-----------------------------------------
- Asegúrate de seleccionar la carpeta correcta antes de iniciar el servidor.
- No cierres el programa mientras el servidor HTTP o el túnel de Cloudflare están activos.
- Si el enlace de Cloudflare deja de funcionar, detén el túnel y vuelve a iniciarlo.
- Para compartir archivos de forma segura, solo proporciona el enlace a personas de confianza.
"""

    # Crear un Text widget para mostrar las instrucciones con más ancho
    text_widget = tk.Text(instructions_window, wrap="word", height=20, width=80)  # ✅ Más ancho
    text_widget.insert("1.0", instrucciones)
    text_widget.config(state="disabled")  # Hace que el texto no sea editable
    text_widget.pack(padx=10, pady=10, expand=True, fill="both")  # ✅ Se ajusta a la ventana

    # Botón para cerrar la ventana de instrucciones
    close_button = tk.Button(instructions_window, text="Cerrar", command=instructions_window.destroy)
    close_button.pack(pady=5)



# Crear la ventana principal
root = tk.Tk()
root.title("PyDataTunnel By Lithiuhm")
root.geometry("640x375")
root.resizable(False, False)  # No permitir redimensionar
root.iconbitmap(ICON_PATH)  # ✅ Aplica el icono a la ventana principal


# ----- BOTÓN DE INSTRUCCIONES (Encima de la etiqueta de carpeta) -----
instructions_button = tk.Button(root, text="ℹ️ Cómo Usar", command=show_instructions, bg="lightblue")
instructions_button.grid(row=0, column=0, columnspan=3, pady=5)

# Etiqueta para la carpeta seleccionada (se mantiene centrada arriba)
dir_label = tk.Label(root, text=f"Carpeta seleccionada: {selected_directory}", wraplength=480)
dir_label.grid(row=1, column=0, columnspan=3, pady=10)

# ----- COLUMNA 1: CONFIGURACIÓN -----
select_button = tk.Button(root, text="📁 Seleccionar Carpeta", command=select_directory)
select_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

download_button = tk.Button(root, text="⬇️ Descargar Cloudflare Tunnel", command=download_cloudflared)
download_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# ----- COLUMNA 2: INICIO -----
start_server_button = tk.Button(root, text="🚀 Iniciar Servidor HTTP", command=start_server)
start_server_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

start_tunnel_button = tk.Button(root, text="🌐 Iniciar Cloudflare Tunnel", command=start_tunnel)
start_tunnel_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

link_button = tk.Button(root, text="🔗 Copiar Enlace", command=copy_link, state=tk.DISABLED)
link_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# ----- COLUMNA 3: ACCIONES DE CIERRE -----
stop_button = tk.Button(root, text="❌ Detener Todo", command=stop_all, bg="red", fg="white")
stop_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

delete_button = tk.Button(root, text="🗑️ Eliminar Cloudflare Tunnel", command=delete_cloudflared, bg="darkred", fg="white")
delete_button.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

# ----- ÁREA DE ESTADO (Mensajes) -----
status_text = tk.Text(root, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED)  # ✅ Más ancho
status_text.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")  # ✅ Se ajusta horizontalmente

# Iniciar la aplicación
root.mainloop()

