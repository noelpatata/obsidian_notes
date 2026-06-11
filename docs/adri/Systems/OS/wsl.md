#wsl #windows #linux #virtualizacion

# Windows Subsystem for Linux (WSL)

Windows Subsystem for Linux es una maquina virtual ligera dentro de Windows, que con Hyper-V (hypervisor) corre Linux dentro de Windows de manera integrada. Es virtualizacion de baja capa.

## Que es WSL?

WSL permite ejecutar un entorno Linux completo directamente en Windows, sin necesidad de una maquina virtual tradicional ni de dual-boot. Se integra nativamente con el sistema de archivos de Windows, permitiendo acceder a archivos de Windows desde Linux y viceversa.

## WSL 1 vs WSL 2

| Aspecto | WSL 1 | WSL 2 |
|---|---|---|
| Arquitectura | Traductor de llamadas syscalls al kernel de Windows | Maquina virtual ligera con kernel Linux real |
| Rendimiento I/O | Lento en operaciones de archivos del sistema de archivos de Windows | Mucho más rápido, especialmente en `git`, `npm`, etc. |
| Compatibilidad | No soporta todas las llamadas al sistema Linux | Compatibilidad completa con binarios Linux nativos |
| Uso de memoria | Menor | Mayor (kernel Linux dedicado) |
| Arranque | Más rápido | Un poco más lento al iniciar |

> [!tip] Recomendación
> Para la mayoría de casos de uso, **WSL 2** es la mejor opción gracias a su rendimiento y compatibilidad completa.

## Instalación

### Requisitos previos

- Windows 10 versión 1903+ o Windows 11.
- Habilitar virtualización en la BIOS (VT-x / AMD-V).
- Habilitar las features de Windows:

```powershell
# PowerShell como Administrador
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### Instalar WSL

```powershell
# Desde PowerShell (como Administrador) - WSL 2
wsl --install

# Instalar una distro específica
wsl --install -d Ubuntu

# Configurar WSL 2 como versión por defecto
wsl --set-default-version 2
```

### Listar distros disponibles

```powershell
wsl --list --online
```

## Comandos básicos de WSL

```powershell
# Listar distros instaladas
wsl --list --verbose

# Iniciar una distro
wsl -d Ubuntu

# Apagar una distro
wsl --terminate Ubuntu

# Actualizar la versión del kernel de WSL 2
wsl --update

# Configurar el usuario por defecto
wsl --set-default-user <username>
```

### Dentro de Linux

```bash
# Acceder al sistema de archivos de Windows desde Linux
cd /mnt/c/Users/usuario/Documents

# Ver las distros disponibles
lsb_release -a
```

### Acceder a Linux desde Windows

```powershell
# Abrir el explorador de archivos en la ruta de la distro Linux
wsl explorer.exe .
```

## Casos de uso

- **Desarrollo**: Ejecutar herramientas de desarrollo Linux (gcc, make, python, node) sin salir de Windows.
- **Pentesting**: Utilizar herramientas como [[nmap-cheatsheet|Nmap]], Metasploit, o Burp Suite en un entorno Linux mientras se usa Windows como sistema principal.
- **Automatización**: Ejecutar scripts bash y automatizaciones Linux directamente en Windows.
- **Contenedores**: Docker Desktop usa WSL 2 como backend para ejecutar contenedores Linux.
- **Investigación de seguridad**: Analizar malware Linux, ejecutar herramientas forenses, o configurar laboratorios de prueba.

## Limitaciones

- No se puede acceder a GPU para machine learning (mejorado en WSL 2).
- Algunas aplicaciones que requieren control total del hardware no funcionan.
- El sistema de archivos Linux se accede mejor desde Linux (`/home/`) que desde Windows (`\\wsl$\`).

## Referencias

- [[networking-config]] para configuración de red dentro de WSL
- [[nmap-cheatsheet]] para uso de Nmap desde WSL
