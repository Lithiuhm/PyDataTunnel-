<h1 align="center">PyDataTunnel - Comparte Archivos de Forma Segura </h1>

<div align="center">
  <img src="https://i.imgur.com/Fxp6szx.png" alt="PyDataTunnel" width="500">
</div>



👀 ¿Alguna vez has necesitado compartir un archivo con alguien rápidamente? Ya sea con un amigo, un compañero de trabajo, un profesor o un familiar, a veces enviar un archivo por correo o subirlo a la nube puede ser lento, incómodo y tardío, además de que tu archivo se puede quedar en la nube de un proveedor tercero.

Con **PyDataTunnel**, compartir archivos nunca ha sido tan fácil. Este programa te permite **crear un servidor HTTP local** y, con la ayuda de **Cloudflare Tunnel** completamente cifrado con la última tecnología de Cloduflare, generar un enlace público accesible desde cualquier parte del mundo, sin necesidad de abrir puertos ni realizar configuraciones complicadas.

---

## 🔹 **¿Cómo funciona?**

1️⃣ **Selecciona una carpeta** con los archivos que deseas compartir.  
2️⃣ **Inicia el servidor HTTP**, que alojará los archivos de forma local.  
3️⃣ **Activa Cloudflare Tunnel** para generar un enlace seguro.  
4️⃣ **Comparte el enlace** con quien quieras, sin necesidad de configuraciones adicionales.  
5️⃣ **Cuando termines, detén el servidor y el túnel** con un solo clic.  

---

## ✨ **Características**

- 🌍 **Comparte archivos fácilmente**, sin subirlos a la nube.  
- 🔒 **Conexión segura** mediante Cloudflare Tunnel y cifrado HTTPS.  
- 🛠️ **Elección de archivos y carpetas**, sin restricciones.  
- ⏳ **Alta velocidad de transferencia**, sin depender de servidores externos.  
- 🖥 **Interfaz gráfica intuitiva y amigable**, sin necesidad de usar la terminal.  
- ⚡ **No requiere apertura de puertos ni configuraciones avanzadas**.  
- ❌ **Detén el servidor y el túnel en cualquier momento** para mayor seguridad.  

---

## 🛡️ **Medidas de Seguridad**

PyDataTunnel prioriza la privacidad y seguridad de tus archivos mediante las siguientes medidas:

- **Cifrado HTTPS**: Todo el tráfico se transmite de forma segura a través de Cloudflare Tunnel, evitando intercepciones de terceros.  
- **No se almacenan datos en servidores externos**: Todo el contenido se mantiene en tu dispositivo y solo es accesible a través del enlace generado.  
- **Elección selectiva de archivos**: Puedes decidir exactamente qué compartir, sin exposiciones innecesarias.  
- **Control total del acceso**: Al detener el servidor o el túnel, eliminas instantáneamente el acceso remoto a los archivos.  

---

## 🤖 **Formas de Uso**

### 🚀 Opción 1: Descargar y ejecutar el `.exe`

1️⃣ **Descarga [`PyDataTunnel.exe`](https://github.com/Lithiuhm/PyDataTunnel/releases)** desde la sección de Releases.  
2️⃣ **Ejecuta `PyDataTunnel.exe`** (no requiere instalación).  
3️⃣ **Sigue los pasos en la interfaz** para compartir archivos rápidamente.  

- Selecciona la carpeta que deseas compartir.
- Descarga el tunnel de Cloudflare usando el botón si no lo tienes todavía
- Inicia el servidor HTTP, que alojará los archivos de forma local.
- Activa Cloudflare Tunnel para generar un enlace de acceso remoto seguro
- Comparte el enlace con quien necesites.
- Cuando termines, detén el servidor y el túnel para cerrar el acceso a los archivos.  
- Borra el tunnel de Cloudflare si no lo vas a volver a usar

### 🐍 Opción 2: Descargar el código fuente y ejecutarlo con Python

1️⃣ **Clona el repositorio o descarga el código fuente:**

```bash
 git clone https://github.com/Lithiuhm/PyDataTunnel.git
 cd PyDataTunnel
```

2️⃣ Instala las dependencias necesarias:

```
 pip install -r requirements.txt
```

3️⃣ Ejecuta el script principal:

```
 python main.py
```

Ahora puedes compartir archivos desde tu propio servidor HTTP con Cloudflare Tunnel. 🎉

---

## 🦖 **Futuras Mejoras**

Para seguir mejorando la seguridad y funcionalidad de PyDataTunnel, tengo implementaciones futuras:

- **Autenticación de usuarios**: Generar un usuario y contraseña aleatorios al iniciar el servidor HTTP, proporcionando estos datos a quien reciba el enlace para restringir el acceso solo a personas autorizadas.
- **Interfaz de gestión avanzada**: Permitir una interfaz web para administrar permisos, controlar sesiones activas y visualizar registros de acceso.
- **Expiración de enlaces**: Implementar un sistema para que los enlaces generados expiren después de un tiempo determinado o tras un número específico de accesos.
- **Interfaz web más intuitiva**: Reemplazar la simple visualización HTTP por una interfaz moderna y amigable con diseño responsivo.

---

**¡Abierto a cualquier ayuda y commentario!**

---

# Descargo de responsabilidad

No me hago cargo del mal uso que se le de a esta aplicación, todo esto es con fines educativos e informativos, gracias y a disfrutarlo!
## Autor

- [@Lithiuhm](https://www.github.com/Lithiuhm)

